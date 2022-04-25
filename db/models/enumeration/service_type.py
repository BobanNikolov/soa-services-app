from enum import Enum


class ServiceType(str, Enum):
    service_vaccination = "VACCINATION"
    service_injection = "INJECTION"
    service_medical_treatment = "MEDICAL_TREATMENT"
    service_walking = "WALKING"
