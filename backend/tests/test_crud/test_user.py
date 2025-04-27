from datetime import date

import pytest
import pytest_asyncio
from fastapi import HTTPException
from pytest_mock import MockFixture
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import UserCrud
from schemas.user import UserCreate, UserUpdate


# 建立 UserCrud 實例
@pytest_asyncio.fixture(scope="function")
async def user_crud(session: AsyncSession) -> UserCrud:
    return UserCrud(session)


# 建立測試用的使用者資料
@pytest.fixture(scope="function")
def user_data_1() -> UserCreate:
    return UserCreate(
        name="Test User",
        email="test@example.com",
        password="password123",
        age=25,
        birthday=date(1998, 8, 8),
        avatar="https://example.com/avatar.jpg",
    )


@pytest.fixture(scope="function")
def user_data_2():
    return UserCreate(
        name="Another User",
        email="another@example.com",
        password="password456",
        age=30,
        birthday=date(1993, 5, 15),
        avatar=None,
    )


@pytest.fixture(scope="function")
def mock_hash_password(mocker: MockFixture) -> None:
    mocker.patch("crud.user.hash_password", autospec=True, side_effect=lambda pw: "hashed_password")


class TestUserCrud:
    # 測試創建使用者
    @pytest.mark.asyncio
    async def test_create_user(
        self, user_crud: UserCrud, user_data_1: UserCreate, mock_hash_password
    ):
        # When
        user = await user_crud.create(user_data_1)
        # Then
        assert user.id is not None
        assert user.name == user_data_1.name
        assert user.email == user_data_1.email
        assert user.age == user_data_1.age
        assert user.birthday == user_data_1.birthday
        assert user.avatar == user_data_1.avatar
        assert user.password == "hashed_password"

    # 測試獲取所有使用者
    @pytest.mark.asyncio
    async def test_get_all(
        self,
        user_crud: UserCrud,
        user_data_1: UserCreate,
        user_data_2: UserCreate,
        mock_hash_password,
    ):
        # Given
        await user_crud.create(user_data_1)
        await user_crud.create(user_data_2)
        # When
        users = await user_crud.get_all()
        # Then
        assert len(users) == 2
        assert users[0].email == user_data_1.email
        assert users[1].email == user_data_2.email

    # 測試透過 ID 獲取使用者
    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        user_crud: UserCrud,
        user_data_1: UserCreate,
        mock_hash_password,
    ):
        # Given
        user = await user_crud.create(user_data_1)
        # When
        retrieved_user = await user_crud.get_by_id(user.id)
        # Then
        assert retrieved_user.id == user.id
        assert retrieved_user.email == user.email
        assert retrieved_user.name == user.name
        assert retrieved_user.age == user.age
        assert retrieved_user.birthday == user.birthday
        assert retrieved_user.avatar == user.avatar

    # 測試透過不存在的 ID 獲取使用者
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, user_crud: UserCrud):
        # Then
        with pytest.raises(HTTPException):
            await user_crud.get_by_id(999)

    # 測試透過 email 獲取使用者
    @pytest.mark.asyncio
    async def test_get_by_email(
        self,
        user_crud: UserCrud,
        user_data_1: UserCreate,
        mock_hash_password,
    ):
        # Given
        await user_crud.create(user_data_1)
        # When
        user = await user_crud.get_by_email(user_data_1.email)
        # Then
        assert user.email == user_data_1.email
        assert user.name == user_data_1.name
        assert user.age == user_data_1.age
        assert user.birthday == user_data_1.birthday
        assert user.avatar == user_data_1.avatar

    # 測試透過不存在的 email 獲取使用者
    @pytest.mark.asyncio
    async def test_get_by_email_not_found(self, user_crud: UserCrud):
        # Then
        with pytest.raises(HTTPException):
            await user_crud.get_by_email("nonexistent@example.com")

    # 測試部分更新使用者資料
    @pytest.mark.asyncio
    async def test_update_partial(
        self,
        mocker: MockFixture,
        user_crud: UserCrud,
        user_data_1: UserCreate,
        mock_hash_password,
    ):
        # Given
        user = await user_crud.create(user_data_1)
        # When
        update_data = UserUpdate(name="Updated Name", age=26)
        updated_user = await user_crud.update_partial(user.id, update_data)
        await user_crud.session.commit()
        # Then
        assert updated_user.name == "Updated Name"
        assert updated_user.age == 26
        assert updated_user.email == user_data_1.email  # 保持不變
        assert updated_user.birthday == user_data_1.birthday  # 保持不變
        assert updated_user.avatar == user_data_1.avatar  # 保持不變

    # 測試更新密碼
    @pytest.mark.asyncio
    async def test_update_password(
        self,
        mocker: MockFixture,
        user_crud: UserCrud,
        user_data_1: UserCreate,
        mock_hash_password,
    ):
        # Given
        user = await user_crud.create(user_data_1)
        # When
        new_password = "newPassword456"
        update_data = UserUpdate(password=new_password)
        updated_user = await user_crud.update_partial(user.id, update_data)
        await user_crud.session.commit()
        # Then
        assert updated_user.password == "hashed_password"  # 密碼應該已被雜湊

    # 測試更新不存在的使用者資料
    @pytest.mark.asyncio
    async def test_update_partial_not_found(
        self,
        user_crud: UserCrud,
        mock_hash_password,
    ):
        # When
        update_data = UserUpdate(name="Updated Name")
        # Then
        with pytest.raises(HTTPException):
            await user_crud.update_partial(999, update_data)

    # 測試刪除使用者
    @pytest.mark.asyncio
    async def test_delete_user(
        self,
        user_crud: UserCrud,
        user_data_1: UserCreate,
        mock_hash_password,
    ):
        # Given
        user = await user_crud.create(user_data_1)
        # When
        await user_crud.delete(user.id)
        await user_crud.session.commit()
        # Then
        with pytest.raises(HTTPException):
            await user_crud.get_by_id(user.id)

    # 測試刪除不存在的使用者
    @pytest.mark.asyncio
    async def test_delete_not_found(self, user_crud: UserCrud):
        # Then
        with pytest.raises(HTTPException):
            await user_crud.delete(999)
