import httpx

async def fetch_product_details(product_id: int) -> dict:
    url = f"https://external.sampleapi.com/products/{product_id}"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
            response.raise_for_status()  # raise if HTTP error
            data = response.json()
            # Ensure price and stock exist, else default
            return {
                "id": data.get("id", product_id),
                "price": data.get("price", 0.0),
                "available_stock": data.get("available_stock", 0)
            }
    except (httpx.HTTPError, httpx.ConnectTimeout):
        # API down or timeout, return default
        return {
            "id": product_id,
            "price": 0.0,
            "available_stock": 0
        }

