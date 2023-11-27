from db.services.db import BaseSQL

from sqlalchemy import Column, String, DateTime, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum as PythonEnum

class ExperienceLevel(PythonEnum):
    SE = 'SE'
    MI = 'MI'
    EX = 'EX'
    EN = 'EN'

class CompanySize(PythonEnum):
    S = 'S'
    M = 'M'
    L = 'L'

class Salary(BaseSQL):
    __tablename__ = "salaries"

    id = Column(Integer, primary_key=True)
    work_year = Column(DateTime)
    experience_level = Column(Enum(ExperienceLevel))
    employment_type = Column(String)
    job_title = Column(String)
    salary = Column(Integer)
    salary_currency = Column(String)
    salary_in_usd = Column(Integer)
    employee_residence = Column(String)
    remote_ratio = Column(Integer)
    company_location = Column(String)
    company_size = Column(Enum(CompanySize))