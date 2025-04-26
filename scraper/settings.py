# Para asegurar codificación UTF-8 en salida JSON
FEED_EXPORT_ENCODING = 'utf-8'

# Activa el pipeline que vamos a definir
ITEM_PIPELINES = {
    'mynews_spider.pipelines.JsonWriterPipeline': 300,
}