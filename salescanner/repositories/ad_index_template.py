class AdIndexTemplate:

    @staticmethod
    def get_index_mapping():
        return {
            "mappings": {
                "properties": {
                    "literacy": {
                        "type": "long"
                    },
                    "upload_time": {
                        "type": "long"
                    },
                    "image_url": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "ignore_above": 256.0,
                                "type": "keyword"
                            }
                        }
                    },
                    "price": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "ignore_above": 256.0,
                                "type": "keyword"
                            }
                        }
                    },
                    "description": {
                        "type": "text",
                        "analyzer": "bulgarian"
                    },
                    "title": {
                        "type": "text",
                        "analyzer": "bulgarian"
                    },
                    "url": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "ignore_above": 256.0,
                                "type": "keyword"
                            }
                        }
                    }
                }  
            }
        }
