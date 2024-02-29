import csv
import json
import pandas as pd

EDU_DATA_FILEPATH = 'data/case_2_data_for_members.json'
EXAM_DATA_FILEPATH = 'data/case_2_reference_without_resume_sorted.json'


class DataHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.edu_data: list[dict] = json.load(open(EDU_DATA_FILEPATH, 'r', encoding='utf-8'))
        self.exam_data: dict = json.load(open(EXAM_DATA_FILEPATH, 'r', encoding='utf-8'))

    def migrate_json_to_pd_data_frame(self):
        data_to_migrate = []
        vacancy_keys = ('uuid', 'name', 'keywords', 'description', 'comment')
        person_keys = ('uuid', 'first_name', 'last_name', 'birth_date', 'country', 'city', 'about')
        # key_skills
        lists_keys = ('experienceItem', 'educationItem', 'languageItem')
        for row in self.edu_data:
            d_v = row['vacancy']
            vacancy_info = [d_v[k].strip() if d_v[k] is not None else d_v[k] for k in vacancy_keys]
            for passed, passed_key in enumerate(('failed_resumes', 'confirmed_resumes')):
                for person in row[passed_key]:
                    person_info = vacancy_info + [person[k].strip() if person[k] is not None else person[k] for k in
                                                  person_keys] + [
                                      person['key_skills'].split(', ') if person['key_skills'] else None]
                    for key in lists_keys:
                        person_info += [[duty for duty in person[key]] if key in person else None]
                    data_to_migrate.append(person_info + [passed])

        data_frame = pd.DataFrame(data_to_migrate,
                                  columns=['v_' + k for k in vacancy_keys] +
                                          ['p_' + k for k in person_keys] + ['p_key_skills'] +
                                          ['p_' + k for k in lists_keys] +
                                          ['passed'])
        return data_frame

    def migrate_json_to_pd_data_frame_draft(self):
        data_to_migrate = []
        data_columns = []
        vacancy_keys = ('uuid', 'name', 'keywords', 'description', 'comment')
        person_keys = ('uuid', 'first_name', 'last_name', 'birth_date', 'country', 'city', 'about')
        # key_skills
        lists_keys = ('experienceItem', 'educationItem', 'languageItem')
        for row in self.edu_data:
            d_v = row['vacancy']
            vacancy_info = [d_v[k].strip() if d_v[k] is not None else d_v[k] for k in vacancy_keys]
            for passed, passed_key in enumerate(('failed_resumes', 'confirmed_resumes')):
                for person in row[passed_key]:
                    person_info = vacancy_info + [person[k].strip() if person[k] is not None else person[k] for k in
                                                  person_keys] + [
                                      person['key_skills'].split(', ') if person['key_skills'] else None]
                    if 'experienceItem' in person:
                        experience_keys = ('starts', 'ends', 'employer', 'city', 'position', 'description')
                        person_info.append([[item[k].strip() if item[k] else None for k in experience_keys] for item in
                                            person['experienceItem']])
                    if 'educationItem' in person:
                        education_keys = ('year', "organization", "faculty", "specialty", "result", "education_type",
                                          "education_level")
                        person_info.append(
                            [[str(item[k]).strip() if item[k] else None for k in education_keys] for item in
                             person['educationItem']])
                    if 'languageItem' in person:
                        person_info.append(person['languageItem'])
                    data_to_migrate.append(person_info)
        print(*data_to_migrate[0], sep='\n')
        columns = (['v_' + k for k in vacancy_keys] +
                   ['p_' + k for k in person_keys] + ['p_key_skills'] +
                   []
                   + ['passed'])
        print(len(columns))


if __name__ == '__main__':
    EDU_DATA_FILEPATH = '../data/case_2_data_for_members.json'
    EXAM_DATA_FILEPATH = '../data/case_2_reference_without_resume_sorted.json'

    dh = DataHandler()
    # print(dh.migrate_json_to_pd_data_frame().to_csv('text.csv', encoding='utf-8', index=False, sep=';'))
