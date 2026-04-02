#!/usr/bin/env python3
"""
Test API endpoints riêng lẻ
"""
import asyncio
import httpx
from app.core.config import settings

async def test_api_endpoints():
    print("🔍 Testing individual API endpoints...")

    base_url = "http://localhost:8000/api/v1"
    headers = {"Authorization": "Bearer fake_token"}  # Token giả để test

    async with httpx.AsyncClient(timeout=10.0) as client:
        # Test 1: Recommendations
        print("\n1. Testing /recommendations/restaurants")
        try:
            res = await client.get(f"{base_url}/recommendations/restaurants", headers=headers)
            print(f"Status: {res.status_code}")
            if res.status_code == 200:
                data = res.json()
                print(f"Response: {data}")
            else:
                print(f"Error: {res.text}")
        except Exception as e:
            print(f"Exception: {e}")

        # Test 2: Restaurants search
        print("\n2. Testing /restaurants (search)")
        try:
            res = await client.get(f"{base_url}/restaurants", params={"search": "nhà hàng", "limit": 5}, headers=headers)
            print(f"Status: {res.status_code}")
            if res.status_code == 200:
                data = res.json()
                print(f"Response: {data}")
            else:
                print(f"Error: {res.text}")
        except Exception as e:
            print(f"Exception: {e}")

        # Test 3: Suggestions heatmap (cần restaurant_id)
        print("\n3. Testing /suggestions/heatmap/1")
        try:
            res = await client.get(f"{base_url}/suggestions/heatmap/1", headers=headers)
            print(f"Status: {res.status_code}")
            if res.status_code == 200:
                data = res.json()
                print(f"Response: {data}")
            else:
                print(f"Error: {res.text}")
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_api_endpoints())