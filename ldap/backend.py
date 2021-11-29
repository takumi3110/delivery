from ssl import CERT_NONE, PROTOCOL_SSLv23
from ldap3 import Server, Connection, NTLM,Tls,SUBTREE
from django.conf import settings
from django.contrib.auth import get_user_model
from user.models import User

class Backend:
    def authenticate(self, request, username=None, password=None):
        s = Server(settings.LDAP_HOST)
        try:
            c = Connection(s,
                        user='{0}\\{1}'.format(settings.LDAP_DOMAIN, username),
                        password=password,
                        authentication=NTLM,
                        auto_bind=True
            )
            user = get_user_model()
            result, created = user.objects.update_or_create(
                username=username,
            )
            sfilter = "(&(objectClass=user)(samAccountName=" + username + "))"
            entry_list = c.extend.standard.paged_search(search_base=settings.LDAP_SEARCH_BASE,
                                                            search_filter=sfilter,
                                                            search_scope=SUBTREE,
                                                            attributes=['displayName',
                                                                        'mail',
                                                                        'department',
                                                                        'title',
                                                                        'memberOf',
                                                            ],
                                                            paged_size=5,
                                                            size_limit=1000,
                                                            generator=False,
                                                            get_operational_attributes=True,
            )
            c.unbind()
            for entry in entry_list:
                if created:
                    result.is_staff = True
                result.screenname = entry['attributes']['displayName']
                result.email = entry['attributes']['mail']
                result.Department = entry['attributes']['department']
                result.Position = entry['attributes']['title']
            result.save()
            return result
        except:
            return None
    def get_user(self, user_id):
        user = get_user_model()
        try:
            return user.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None