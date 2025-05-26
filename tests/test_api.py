class HeadHunterAPI(JobPlatformAPI):
    def get_employer(self, employer_id: str) -> Dict:
        url = f"https://api.hh.ru/employers/{employer_id}"
        response = requests.get(url, headers=self._headers)
        response.raise_for_status()
        return response.json()

    def get_employer_vacancies(self, employer_id: str) -> List[Dict]:
        url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
        response = requests.get(url, headers=self._headers)
        response.raise_for_status()
        return response.json()['items']
