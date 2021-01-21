import os
import json

# from attr import asdict
from ldap3.core.exceptions import LDAPExceptionError

from pb import app, db
from ldap3 import Connection, Server, MOCK_SYNC, RESTARTABLE

from pb.ldap.ldap import LdapModel, LdapSchema


# class PBError(Exception):
#     pass
#
#
# ApiError = PBError


class LdapService(object):
    search_base = "ou=People,o=University of Virginia,c=US"
    attributes = ['uid', 'cn', 'sn', 'displayName', 'givenName', 'mail', 'objectClass', 'UvaDisplayDepartment',
                  'telephoneNumber', 'title', 'uvaPersonIAMAffiliation', 'uvaPersonSponsoredType']
    # uid_search_string = "(&(objectclass=person)(uid=%s))"
    # user_or_last_name_search = "(&(objectclass=person)(|(uid=%s*)(sn=%s*)))"
    # cn_single_search = '(&(objectclass=person)(cn=%s*))'
    # cn_double_search = '(&(objectclass=person)(&(cn=%s*)(cn=*%s*)))'
    live_search = '(&(objectclass=person)(|(cn=*%s*)(displayName=*%s*)(givenName=*%s*)(mail=*%s*)))'
    temp_cache = {}
    conn = None

    @staticmethod
    def __get_conn():
        if not LdapService.conn:
            if app.config['TESTING'] or app.config['LDAP_URL'] == 'mock':
                server = Server('my_fake_server')
                conn = Connection(server, client_strategy=MOCK_SYNC)
                file_path = os.path.abspath(os.path.join(app.root_path, 'pb', 'ldap', 'ldap_response.json'))
                conn.strategy.entries_from_json(file_path)
                conn.bind()
            else:
                server = Server(app.config['LDAP_URL'], connect_timeout=app.config['LDAP_TIMEOUT_SEC'])
                conn = Connection(server, auto_bind=True,
                                       receive_timeout=app.config['LDAP_TIMEOUT_SEC'],
                                       client_strategy=RESTARTABLE)
            LdapService.conn = conn
        return LdapService.conn


    # @staticmethod
    # def user_info(uva_uid):
    #     user_info = db.session.query(LdapModel).filter(LdapModel.uid == uva_uid).first()
    #     if not user_info:
    #         app.logger.info("No cache for " + uva_uid)
    #         search_string = LdapService.uid_search_string % uva_uid
    #         conn = LdapService.__get_conn()
    #         conn.search(LdapService.search_base, search_string, attributes=LdapService.attributes)
    #         if len(conn.entries) < 1:
    #             raise ApiError("missing_ldap_record", "Unable to locate a user with id %s in LDAP" % uva_uid)
    #         entry = conn.entries[0]
    #         user_info = LdapModel.from_entry(entry)
    #         db.session.add(user_info)
    #         db.session.commit()
    #     return user_info

    @staticmethod
    def search_users(query, limit):
        query = query.strip()
        if len(query) < 3:
            return []
        else:
            # Search cn, displayName, givenName and mail
            search_string = LdapService.live_search % (query, query, query, query)
        results = []
        app.logger.info(search_string)
        try:
            conn = LdapService.__get_conn()
            conn.search(LdapService.search_base, search_string, attributes=LdapService.attributes)
            # Entries are returned as a generator, accessing entries
            # can make subsequent calls to the ldap service, so limit
            # those here.
            count = 0
            for entry in conn.entries:
                if count > limit:
                    break
                results.append(LdapSchema().dump(LdapModel.from_entry(entry)))
                count += 1
        except LDAPExceptionError as le:
            app.logger.info("Failed to execute ldap search. %s", str(le))

        return results

    def users_as_json(needle):
        users = []
        if len(needle) > 2:
            result = LdapService.search_users(needle, 15)
            for user in result:
                users.append({'uid': user['uid'], 'display_name': user['display_name']})
        return json.dumps(users)

