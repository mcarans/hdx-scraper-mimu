#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Unit tests for mimu.

'''
from os.path import join

import pytest
from hdx.hdx_configuration import Configuration
from hdx.hdx_locations import Locations
from hdx.location.country import Country
from hdx.utilities.path import temp_dir
from hdx.data.vocabulary import Vocabulary
from mimu import generate_dataset_and_showcase, get_layersdata


class TestMIMU:
    layersdata = [{"abstract": "Towns are urban areas divided into wards.", "category__gn_description": "Location",
"csw_type": "dataset",
"csw_wkt_geometry": "POLYGON(456)", "date": "2019-08-05T22:06:00", 
"detail_url": "/layers/geonode%3Ammr_town_2019_july", "distribution_description": "Web address (URL)",
"distribution_url": "http://geonode.themimu.info/layers/geonode%3Ammr_town_2019_july", "id": 211,
"owner__username": "phyokyi", "popular_count": 126, "rating": 0, "share_count": 0, "srid": "EPSG:4326",
"supplemental_information": "Place name from GAD, transliteration by MIMU. Names available in Myanmar Unicode 3 and Roman script.",
"thumbnail_url": "http://geonode.themimu.info/uploaded/thumbs/layer-3bc1761a-b7f7-11e9-9231-42010a80000c-thumb.png",
"title": "Myanmar Town 2019 July", "uuid": "3bc1761a-b7f7-11e9-9231-42010a80000c"},
{"abstract": "A Landsat-based classification of Myanmar’s forest cover",
"category__gn_description": None, "csw_type": "dataset",
"csw_wkt_geometry": "POLYGON(567)", "date": "2019-02-12T11:12:00",
"detail_url": "/layers/geonode%3Amyan_lvl2_smoothed_dec2015_resamp",
"distribution_description": "Web address (URL)",
"distribution_url": "http://geonode.themimu.info/layers/geonode%3Amyan_lvl2_smoothed_dec2015_resamp",
"id": 173, "owner__username": "EcoDev-ALARM", "popular_count": 749, "rating": 0, "share_count": 0,
"srid": "EPSG:4326", "supplemental_information": "LAND COVER CLASSES",
"thumbnail_url": "http://geonode.themimu.info/uploaded/thumbs/layer-5801f3fa-2ee9-11e9-8d0e-42010a80000c-thumb.png",
"title": "Myanmar 2002-2014 Forest Cover Change", "uuid": "5801f3fa-2ee9-11e9-8d0e-42010a80000c"}]

    @pytest.fixture(scope='function')
    def configuration(self):
        Configuration._create(hdx_read_only=True, user_agent='test',
                              project_config_yaml=join('tests', 'config', 'project_configuration.yml'))
        Locations.set_validlocations([{'name': 'mmr', 'title': 'Myanmar'}])  # add locations used in tests
        Country.countriesdata(False)
        Vocabulary._tags_dict = True
        Vocabulary._approved_vocabulary = {'tags': [{'name': 'populated places - settlements'}, {'name': 'land use and land cover'}], 'id': '4e61d464-4943-4e97-973a-84673c1aaa87', 'name': 'approved'}

    @pytest.fixture(scope='function')
    def downloader(self):
        class Response:
            @staticmethod
            def json():
                pass

        class Download:
            @staticmethod
            def download(url):
                response = Response()
                if url == 'http://xxx/api/layers':
                    def fn():
                        return {'objects': TestMIMU.layersdata}
                    response.json = fn
                return response
        return Download()

    def test_get_layersdata(self, downloader):
        layersdata = get_layersdata('http://xxx/', downloader)
        assert layersdata == TestMIMU.layersdata

    def test_generate_dataset_and_showcase(self, configuration):
        dataset, showcase = generate_dataset_and_showcase('http://xxx/', TestMIMU.layersdata[0])
        assert dataset == {'name': 'mimu-myanmar-town-2019-july', 'title': 'Myanmar Town 2019 July',
                           'notes': 'Towns are urban areas divided into wards.\n\nPlace name from GAD, transliteration by MIMU. Names available in Myanmar Unicode 3 and Roman script.',
                           'maintainer': '196196be-6037-4488-8b71-d786adf4c081', 'owner_org': 'bde18602-2e92-462a-8e88-a0018a7b13f9', 'dataset_date': '08/05/2019',
                           'data_update_frequency': '-2', 'subnational': '1', 'groups': [{'name': 'mmr'}], 'tags': [{'name': 'populated places - settlements', 'vocabulary_id': '4e61d464-4943-4e97-973a-84673c1aaa87'}]}
        resources = dataset.get_resources()
        assert resources == [{'name': 'Myanmar Town 2019 July shapefile', 'url': 'http://xxx/geoserver/wfs?format_options=charset:UTF-8&typename=geonode%3Ammr_town_2019_july&outputFormat=SHAPE-ZIP&version=1.0.0&service=WFS&request=GetFeature',
                              'description': 'Zipped Shapefile. Towns are urban areas divided into wards.', 'format': 'zipped shapefile', 'resource_type': 'api', 'url_type': 'api'},
                             {'name': 'Myanmar Town 2019 July geojson', 'url': 'http://xxx/geoserver/wfs?srsName=EPSG%3A4326&typename=geonode%3Ammr_town_2019_july&outputFormat=json&version=1.0.0&service=WFS&request=GetFeature',
                              'description': 'GeoJSON file. Towns are urban areas divided into wards.', 'format': 'geojson', 'resource_type': 'api', 'url_type': 'api'}]
        assert showcase == {'name': 'mimu-myanmar-town-2019-july-showcase', 'title': 'Myanmar Town 2019 July', 'notes': 'Towns are urban areas divided into wards.',
                            'url': 'http://geonode.themimu.info/layers/geonode%3Ammr_town_2019_july', 'image_url': 'http://geonode.themimu.info/uploaded/thumbs/layer-3bc1761a-b7f7-11e9-9231-42010a80000c-thumb.png',
                            'tags': [{'name': 'populated places - settlements', 'vocabulary_id': '4e61d464-4943-4e97-973a-84673c1aaa87'}]}

        dataset, showcase = generate_dataset_and_showcase('http://xxx/', TestMIMU.layersdata[1])
        assert dataset == {'name': 'mimu-myanmar-2002-2014-forest-cover-change', 'title': 'Myanmar 2002-2014 Forest Cover Change',
                           'notes': 'A Landsat-based classification of Myanmar’s forest cover\n\nLAND COVER CLASSES',
                           'maintainer': '196196be-6037-4488-8b71-d786adf4c081', 'owner_org': 'bde18602-2e92-462a-8e88-a0018a7b13f9', 'dataset_date': '02/12/2019',
                           'data_update_frequency': '-2', 'subnational': '1', 'groups': [{'name': 'mmr'}], 'tags': [{'name': 'land use and land cover', 'vocabulary_id': '4e61d464-4943-4e97-973a-84673c1aaa87'}]}
        resources = dataset.get_resources()
        assert resources == [{'name': 'Myanmar 2002-2014 Forest Cover Change shapefile', 'url': 'http://xxx/geoserver/wfs?format_options=charset:UTF-8&typename=geonode%3Amyan_lvl2_smoothed_dec2015_resamp&outputFormat=SHAPE-ZIP&version=1.0.0&service=WFS&request=GetFeature',
                              'description': 'Zipped Shapefile. A Landsat-based classification of Myanmar’s forest cover', 'format': 'zipped shapefile', 'resource_type': 'api', 'url_type': 'api'},
                             {'name': 'Myanmar 2002-2014 Forest Cover Change geojson', 'url': 'http://xxx/geoserver/wfs?srsName=EPSG%3A4326&typename=geonode%3Amyan_lvl2_smoothed_dec2015_resamp&outputFormat=json&version=1.0.0&service=WFS&request=GetFeature',
                              'description': 'GeoJSON file. A Landsat-based classification of Myanmar’s forest cover', 'format': 'geojson', 'resource_type': 'api', 'url_type': 'api'}]
        assert showcase == {'name': 'mimu-myanmar-2002-2014-forest-cover-change-showcase', 'title': 'Myanmar 2002-2014 Forest Cover Change',
                            'notes': 'A Landsat-based classification of Myanmar’s forest cover', 'url': 'http://geonode.themimu.info/layers/geonode%3Amyan_lvl2_smoothed_dec2015_resamp',
                            'image_url': 'http://geonode.themimu.info/uploaded/thumbs/layer-5801f3fa-2ee9-11e9-8d0e-42010a80000c-thumb.png',
                            'tags': [{'name': 'land use and land cover', 'vocabulary_id': '4e61d464-4943-4e97-973a-84673c1aaa87'}]}
