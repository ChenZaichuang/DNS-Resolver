import dns.resolver
import gevent

from python_utils.thread_pool import ThreadPool


class DNSResolver:

    def __init__(self, dns_servers=None):
        self.dns_servers = dns_servers or ['119.29.29.29',
                                           '182.254.116.116',
                                           '114.114.114.114',
                                           '223.5.5.5',
                                           '223.6.6.6',
                                           '180.76.76.76',
                                           '9.9.9.9',
                                           '8.8.8.8']
        self.pool = ThreadPool(total_thread_number=len(self.dns_servers))

    def _get_ip_from_dns_server(self, host, dns_server, print_error=False, timeout=5):
        try:
            with gevent.Timeout(timeout):
                resolver = dns.resolver.Resolver()
                resolver.nameservers = [dns_server]
                answers = resolver.query(host, 'A')
                return {answer.to_text() for answer in answers}
        except gevent.timeout.Timeout:
            if print_error:
                print(f'Timeout to get ip of {host} from {dns_server}')
            return set()
        except (dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
            if print_error:
                print(f'No ip found for {host} from {dns_server}')
            return set()

    def get_ip_list_of_host(self, host, print_error=False, timeout=5):
        pool = self.pool.new_pool_status()
        for dns_server in self.dns_servers:
            pool.apply_async(self._get_ip_from_dns_server, args=(host, dns_server), kwds=dict(print_error=print_error, timeout=timeout))
        results = pool.get_results_order_by_index()
        all_ips = set()
        for ip_set in results:
            all_ips |= ip_set
        return all_ips


if __name__ == '__main__':
    ips = DNSResolver().get_ip_list_of_host('0.tcp.ngrok.io')
    print(ips)