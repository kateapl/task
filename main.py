from aiohttp import web
import json
from client import SingletonClient
from bson import json_util, objectid
from loguru import logger


routes = web.RouteTableDef()


@routes.post('/create_item')
async def create_item(request: web.Request):
    """get json
       returns status"""
    params = await request.json()
    logger.info(params)
    if not (params.get('title') and params.get('description')):
        return web.json_response({'error': 'title or description is not specified'}, status=422)

    db = SingletonClient.get_data_base()
    result = await db.products.insert_one(dict(params))
    if result:
        return web.json_response({'status': 'product was added'}, status=200)


@routes.get('/get_items')
async def get_items(request: web.Request):
    """get sort field
        returns sorted list of product titles
        or items from db"""
    try:
        params = await request.json()
    except json.decoder.JSONDecodeError:
        params = {}
    logger.info(params)
    db = SingletonClient.get_data_base()
    cursor = db.products.find({})

    if params.get('sort'):
        cursor = cursor.sort(params.get('sort'))
        list_products = await cursor.to_list(length=await db.products.count_documents({}))
        titles = [item['title'] for item in list_products]
        jsn = json_util.dumps({'sorted_products': titles})
        return web.Response(text=jsn, headers={'Content-Type': 'application / json'}, status=200)

    list_products = await cursor.to_list(length=await db.products.count_documents({}))
    jsn = json_util.dumps({'products': list_products})

    return web.Response(text=jsn, headers={'Content-Type': 'application / json'}, status=200)


@routes.get('/get_filter')
async def get_items_titles(request: web.Request):
    """get filter field
    returns filtered list of product titles"""
    try:
        params = await request.json()
    except json.decoder.JSONDecodeError:
        params = {}
    logger.info(params)

    db = SingletonClient.get_data_base()
    try:
        key = list(params.keys())[0]
        cursor = db.products.find({
            key: params.get(key)
        })
    except IndexError:
        cursor = db.products.find({})

    products_list = await cursor.to_list(length=await db.products.count_documents({}))
    logger.info(products_list)
    if not products_list:
        return web.json_response({'error': 'products not found'}, status=404)

    products_list = [item['title'] for item in products_list]

    jsn = json_util.dumps({'titles': products_list})
    return web.Response(text=jsn, headers={'Content-Type': 'application / json'}, status=200)


@routes.get('/get_item')
async def get_item(request: web.Request):
    """get item by id
    returns all item fields"""
    params = await request.json()
    logger.info(params)

    db = SingletonClient.get_data_base()
    _id = params['_id']
    try:
        _id = objectid.ObjectId(_id)
    except KeyError:
        return web.json_response({'error': '_id is not specified'}, status=422)

    result = await db.products.find_one({
        '_id': _id
    })

    if not result:
        return web.json_response({'error': 'item not found'}, status=404)

    jsn = json_util.dumps({'item': result})
    return web.Response(text=jsn, headers={'Content-Type': 'application / json'}, status=200)


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app)
