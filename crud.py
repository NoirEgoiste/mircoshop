import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.engine import Result
from core.db import db_session
from core.models import Post, Profile, User


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print("user", user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    # result: Result = await session.execute(stmt)
    # user: User | None = result.scalar_one_or_none()
    # user: User | None = result.scalar_one_()
    user: User | None = await session.scalar(stmt)
    print("found user", username, user)
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Profile:
    profile = Profile(
        user_id=user_id,
        firstname=first_name,
        lastname=last_name,
    )
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession):
    stmt = (
        select(User)
        .where(User.profile)
        .options(joinedload(User.profile))
        .order_by(User.id)
    )
    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        print(user.profile.firstname)


async def create_posts(
    session: AsyncSession,
    user_id,
    *posts_titles: str,
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in posts_titles]
    session.add_all(posts)
    print(posts)
    await session.commit()


async def get_users_with_posts(
    session: AsyncSession,
):
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    stmt = (
        select(User)
        .options(
            # joinedload(User.posts),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
    # users = await session.scalars(stmt)
    # result: Result = await session.execute(stmt)
    # # users = result.unique().scalars()
    # users = result.scalars()
    users = await session.scalars(stmt)

    # for user in users.unique():  # type: User
    for user in users:  # type: User
        print("**" * 10)
        print(user)
        for post in user.posts:
            print("-", post)


async def get_posts_with_authors(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)

    for post in posts:
        print("post", post)
        print("author", post.user)


async def get_users_with_posts_and_profiles(
    session: AsyncSession,
):
    stmt = (
        select(User)
        .options(
            joinedload(User.profile),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
    users = await session.scalars(stmt)

    for user in users:  # type: User
        print("**" * 10)
        print(user, user.profile and user.profile.firstname)
        for post in user.posts:
            print("-", post)


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        .options(
            joinedload(Profile.user).selectinload(User.posts),
        )
        .order_by(Profile.id)
    )
    profiles = await session.scalars(stmt)
    for profile in profiles:
        print(profile.firstname, profile.user)
        print(profile.user.posts)


async def main():
    async with db_session.session_factory() as session:
        # await create_user(session=session, username="sol")
        # await create_user(session=session, username="andre")
        # user_sol = await get_user_by_username(session, "sol")
        # user_sam = await get_user_by_username(session=session, username="sam")
        # user_sara = await get_user_by_username(session=session, username="sara")
        # # user_max = await get_user_by_username(session=session, username="max")
        # await create_user_profile(
        #     session=session,
        #     user_id=user_sam.id,
        #     first_name="Sam",
        #     last_name="Jackson",
        # )
        # await create_user_profile(
        #     session=session,
        #     user_id=user_sara.id,
        #     first_name="Sara",
        #     last_name="Yohombovich",
        # )
        # await show_users_with_profiles(session=session)
        # await create_posts(
        #     session,
        #     user_sam.id,
        #     "SQLA 2.0",
        #     "SQLA Joins",
        # )
        # await create_posts(
        #     session,
        #     user_sara.id,
        #     "FastAPI intro",
        #     "FastApi more",
        # )
        # await create_posts(
        #     session,
        #     user_sol.id,
        #     "Django intro",
        #     "Django pro",
        # )
        # await get_users_with_posts(session)
        # await get_posts_with_authors(session)
        # await get_users_with_posts_and_profiles(session)
        await get_profiles_with_users_and_users_with_posts(session=session)


if __name__ == "__main__":
    asyncio.run(main())
