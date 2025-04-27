import json
import random
from collections.abc import Callable
from datetime import datetime
from functools import wraps

from locust import HttpUser, between, task


def ensure_login(func: Callable[["WebsiteUser"], bool]):
    @wraps(func)
    def wrapper(self: "WebsiteUser", *args, **kwargs):
        # 確保 login
        if not hasattr(self, "headers"):
            while not self.login():
                self.login()
        # 執行 task
        expired = func(self, *args, **kwargs)
        # 替換過期 access token
        if expired:
            while not self.refresh():
                self.refresh()

    return wrapper


class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    serial_num = 1

    def on_start(self):
        while not self.create_user():
            self.create_user()
        self.login()

    def create_user(self) -> bool:
        self.name = f"CrazyFriday{WebsiteUser.serial_num}"
        self.email = f"user{WebsiteUser.serial_num}@example.com"
        self.password = "securePass123"
        self.age = random.randint(18, 60)
        self.birthday = datetime(1990, 1, 1).strftime("%Y-%m-%d")
        self.item_ids: list[int] = []
        WebsiteUser.serial_num += 1
        payload = {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "age": self.age,
            "birthday": self.birthday,
        }
        with self.client.post(
            "/api/users",
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            catch_response=True,
        ) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure("create_user failed")
            return response.status_code == 201

    def login(self) -> bool:
        payload = {
            "username": self.email,
            "password": self.password,
            "grant_type": "password",
        }
        with self.client.post("/api/auth/login", data=payload, catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                self.access_token = data["access_token"]
                self.refresh_token = data["refresh_token"]
                self.headers = {
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json",
                }
            else:
                response.failure("Login failed")

            return response.status_code == 200

    def refresh(self) -> bool:
        self.headers = {
            "Authorization": f"Bearer {self.refresh_token}",
            "Content-Type": "application/json",
        }
        with self.client.post(
            "/api/auth/refresh", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
                data = response.json()
                self.access_token = data["access_token"]
                self.refresh_token = data["refresh_token"]
                self.headers = {
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json",
                }
            else:
                response.failure("Refresh failed")

            return response.status_code == 200

    @task(3)
    @ensure_login
    def get_all_items(self) -> bool:
        with self.client.get(
            "/api/items?page=1&page_size=10", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code == 200 or response.status_code == 401:
                response.success()
            else:
                response.failure("get_all_items failed")
            return response.status_code == 401

    @task(5)
    @ensure_login
    def create_item(self) -> bool:
        item = {
            "name": "pressure-cooker",
            "price": round(random.uniform(10, 1000), 2),
            "brand": "Prestige",
            "description": "This is an auto-generated item!",
            "stock": random.randint(1, 100),
        }
        with self.client.post(
            "/api/items", headers=self.headers, data=json.dumps(item), catch_response=True
        ) as response:
            if response.status_code == 201:
                response.success()
                item_id: int = response.json()["id"]
                self.item_ids.append(item_id)
            elif response.status_code == 401:
                response.success()
            else:
                response.failure("create_item failed")
            return response.status_code == 401

    @task(2)
    @ensure_login
    def get_item_by_id(self) -> bool:
        if self.item_ids:
            item_id = random.choice(self.item_ids)
            with self.client.get(
                f"/api/items/{item_id}", headers=self.headers, catch_response=True
            ) as response:
                if response.status_code == 200 or response.status_code == 401:
                    response.success()
                else:
                    response.failure("get_item_by_id failed")
                return response.status_code == 401

    @task(2)
    @ensure_login
    def update_item(self) -> bool:
        if self.item_ids:
            item_id = random.choice(self.item_ids)
            update_data = {
                "description": "Update description!",
                "stock": random.randint(1, 50),
            }
            with self.client.patch(
                f"/api/items/{item_id}",
                headers=self.headers,
                data=json.dumps(update_data),
                catch_response=True,
            ) as response:
                if response.status_code == 200 or response.status_code == 401:
                    response.success()
                else:
                    response.failure("get_item_by_id failed")
                return response.status_code == 401

    @task(1)
    @ensure_login
    def delete_item(self) -> bool:
        if self.item_ids:
            item_id = random.choice(self.item_ids)
            with self.client.delete(
                f"/api/items/{item_id}", headers=self.headers, catch_response=True
            ) as response:
                if response.status_code == 204:
                    response.success()
                    self.item_ids.remove(item_id)
                elif response.status_code == 401:
                    response.success()
                else:
                    response.failure("get_item_by_id failed")
                return response.status_code == 401

    @task(1)
    @ensure_login
    def get_all_users(self) -> bool:
        with self.client.get("/api/users", headers=self.headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            return False
