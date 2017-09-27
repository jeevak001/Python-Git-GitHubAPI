import json
import base64
import urllib.request
from urllib.error import HTTPError
class Github(object):
    def __init__(self, user, passwd):
        """
        :param user: User name of github
        :param passwd: Pass word of github
        :return:
        """
        self.__user = user
        self.__passwd = passwd
    # Obtain repositories list
    def list_repos(self):
        """
        :return: A python object contains all repositories information
        """
        request = self.__request('https://api.github.com/user/repos')
        result = urllib.request.urlopen(request).read().decode('utf-8')
        result = json.loads(result)
        return result
    def __request(self, url, method=None):
        request = urllib.request.Request(url, method=method)
        auth = base64.encodebytes(str(('%s:%s' % (self.__user, self.__passwd))).encode('utf-8'))
        auth = auth.decode('utf-8').replace('\n', '')
        request.add_header('Authorization', 'Basic %s' % auth)
        return request
    # Delete all github repos
    def remove_repos(self):
        """
        :return: None
        """
        repos = self.list_repos()
        
        #Disabled repositories need to be skipped in order to prevent the loop being interrupted.
        skip_count = 0
        while len(repos) != skip_count:
            for repo in repos:
                repo_name = repo['name']
                repo_url = 'repos/' + self.__user + '/' + repo_name
                request = self.__request('https://api.github.com/' + repo_url, 'DELETE')
                try:
                    response = urllib.request.urlopen(request)
                    if response.code == 204:
                        print('repo %s has been successfully deleted' % repo['name'])
                    else:
                        return response.code
                except HTTPError as error:
                    if error.code == 403:
                        print('Repository %s is unavailable due to DMCA takedown.' % repo_name)
                        skip_count += 1
                    else:
                        raise error
            repos = self.list_repos()


jeeva = Github("","")
jeeva.remove_repos()