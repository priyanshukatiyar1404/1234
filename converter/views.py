import requests
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import io
from django.http import JsonResponse
from .serializers import InputSerializer
import cloudinary.uploader
from rest_framework import status

import cloudinary
import cloudinary.api
from django.conf import settings

cloudinary.config(
  cloud_name = settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
  api_key = settings.CLOUDINARY_STORAGE['API_KEY'],
  api_secret = settings.CLOUDINARY_STORAGE['API_SECRET']
)



class CSVConvertAPIView(CreateAPIView):
    serializer_class = InputSerializer

    def post(self, request, *args, **kwargs):
        try:
            input_file = request.data.get('input')

            # Read the labor drive report
            labor_drive_report = pd.read_excel(input_file)

            payroll_import_data = pd.DataFrame()

            # Assign values to the payroll import data
            payroll_import_data['emp'] = labor_drive_report['Employee ID'] if 'Employee ID' in labor_drive_report.columns else None
            payroll_import_data['type'] = 1
            payroll_import_data['otmult'] = 1
            payroll_import_data['class'] = None
            payroll_import_data['job'] = None
            payroll_import_data['phase'] = None
            payroll_import_data['cat'] = None
            payroll_import_data['department'] = None
            payroll_import_data['worktype'] = None
            payroll_import_data['unionloc'] = None
            payroll_import_data['billat'] = None
            payroll_import_data['hours'] = labor_drive_report['Labor + Drive'] if 'Labor + Drive' in labor_drive_report.columns else None
            payroll_import_data['rate'] = None
            payroll_import_data['amount'] = None

            # Convert the date format
            if 'Job Created At' in labor_drive_report.columns:
                payroll_import_data['date'] = pd.to_datetime(labor_drive_report['Job Created At'], format='%m/%d/%Y %I:%M %p').dt.strftime('%m/%d/%Y')
            else:
                payroll_import_data['date'] = None

            payroll_import_data['des1'] = None
            payroll_import_data['des2'] = None
            payroll_import_data['wcomp1'] = None
            payroll_import_data['wcomp2'] = None
            payroll_import_data['state'] = None
            payroll_import_data['local'] = None
            payroll_import_data['units'] = None
            payroll_import_data['costtype'] = None
            payroll_import_data['costcode'] = None
            payroll_import_data['equipnum'] = None
            payroll_import_data['equipcode'] = None
            payroll_import_data['equiporder'] = None
            payroll_import_data['equiphours'] = None
            payroll_import_data['equipdes'] = None
            payroll_import_data['account'] = None
            payroll_import_data['starttime'] = None
            payroll_import_data['endtime'] = None

                # Filter out rows where 'emp' or 'hours' is None or NaN
            payroll_import_data = payroll_import_data.dropna(subset=['emp', 'hours']).reset_index(drop=True)
            
            # Save the payroll import data to a CSV file in memory
            output = io.BytesIO()
            payroll_import_data.to_csv(output, index=False)
            output.seek(0)
            
            # Upload the CSV file to Cloudinary
            result = cloudinary.uploader.upload(output, resource_type='raw', folder='csv_converter', format='csv')
            file_url = result['url']
            
            return JsonResponse({'file_url': file_url}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
