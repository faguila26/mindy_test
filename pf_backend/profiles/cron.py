import requests
from django_cron import CronJobBase, Schedule
import logging
from django.db import IntegrityError
from profiles.models import UserProfile  # Ya existente

logger = logging.getLogger('django')
file_handler = logging.FileHandler('C:/Users/Howls/Desktop/Feli/Desarrollo de Software/mindy_test/pf_backend/cron.log')
file_handler.setLevel(logging.DEBUG)  # Puedes cambiar esto a INFO si prefieres menos detalles
logger.addHandler(file_handler)
logger.removeHandler(logger.handlers[0])

class FetchAndStoreProfilesCronJob(CronJobBase):
    schedule = Schedule(run_every_mins=1)
    code = 'profiles.fetch_and_store_profiles_cronjob'

    def do(self):
        logger.info("Iniciando la petición a las APIs para obtener los perfiles.")

        # --------- PRIMERA API ---------
        response_api_1 = requests.get(
            'https://www.mindy.cl/wp-json/mindy/v2/profiles?professionals=true&psychologists=true&professionals_extras=true&get_fonasa=true'
        )
        perfiles_api_1 = {}
        if response_api_1.status_code == 200:
            data_1 = response_api_1.json()
            profiles_api_1 = data_1.get('results', [])
            perfiles_api_1 = {
                perfil.get('email'): perfil.get('next_available_slot')
                for perfil in profiles_api_1 if 'email' in perfil and 'next_available_slot' in perfil
            }
            logger.info(f"API 1 - Perfiles filtrados: {len(perfiles_api_1)}")
        else:
            logger.error(f"API 1 - Error en la respuesta: {response_api_1.status_code}")

        # --------- SEGUNDA API ---------
        response_api_2 = requests.get('https://fonasa.mindy.cl/api.php')
        emails_api_2 = set()
        next_hour_api_2 = {}  # Diccionario para almacenar los next_hour de la API 2
        if response_api_2.status_code == 200:
            data_2 = response_api_2.json()
            profiles_api_2 = data_2.get('data', [])
            for perfil in profiles_api_2:
                email = perfil.get('email')
                next_hour = perfil.get('next_hour')  # Asumimos que 'next_hour' es el valor esperado
                if email and next_hour:
                    emails_api_2.add(email)
                    next_hour_api_2[email] = next_hour
            logger.info(f"API 2 - Perfiles filtrados: {len(emails_api_2)}")
        else:
            logger.error(f"API 2 - Error en la respuesta: {response_api_2.status_code}")

        # --------- MATCH ---------
        emails_comunes = set(perfiles_api_1.keys()) & emails_api_2
        logger.info(f"Perfiles en ambas APIs: {len(emails_comunes)}")

        for email in emails_comunes:
            next_available_slot_api_1 = perfiles_api_1.get(email)
            next_hour_api_2_value = next_hour_api_2.get(email)

            # Revisar qué valores estamos recibiendo
            logger.info(f"Procesando perfil: {email}, next_available_slot_api_1: {next_available_slot_api_1}, next_hour_api_2: {next_hour_api_2_value}")

            # Solo guardamos el email y next_hour
            if next_hour_api_2_value:
                try:
                    # Intentar obtener o crear el perfil
                    logger.info(f"Intentando obtener o crear perfil para {email}")
                    obj, created = UserProfile.objects.get_or_create(
                        email=email,
                        defaults={'next_hour': next_hour_api_2_value}
                    )
                    if created:
                        logger.info(f"Nuevo perfil registrado para {email} con next_hour: {next_hour_api_2_value}")
                    else:
                        logger.info(f"Perfil actualizado para {email} con next_hour: {next_hour_api_2_value}")

                except IntegrityError as e:
                    logger.error(f"Error al crear/actualizar perfil para {email}: {e}")
                except Exception as e:
                    logger.error(f"Error inesperado al procesar el perfil {email}: {e}")
        
        logger.info("Proceso completado.")
