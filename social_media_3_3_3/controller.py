import sqlalchemy as sa
import sqlalchemy.orm as so
import pyinputplus as pyip

from social_media_3_3_3.models import User, Post, Comment, likes_table


class Controller:
    def __init__(self, db_location = 'sqlite:///social_media.db'):
        self.current_user = None
        self.engine = sa.create_engine(db_location)

    def set_current_user_from_name(self, name):
        with so.Session(bind=self.engine) as session:
            self.current_user = session.scalars(sa.select(User).where(User.name == name)).one_or_none()

    def get_user_names(self) -> list[str]:
        with so.Session(bind=self.engine) as session:
            user_names = session.scalars(sa.select(User.name).order_by(User.name)).all()
        return list(user_names)

    def create_user(self,name:str, age:int, gender:str, nationality:str) -> User:
        with so.Session(bind=self.engine) as session:
            user = User(name=name, age=age, gender=gender, nationality=nationality)
            session.add(user)
            session.commit()
            self.current_user = user
        return user

    def get_posts(self, user_name:str)->list[dict]:
        with so.Session(bind=self.engine) as session:
            user= session.scalars(sa.select(User).where(User.name == user_name)).one_or_none()
            posts_info = [{'title':post.title,
                          'description':post.description,
                           'number_likes':len(post.liked_by_users),
                           'comments': [{'user': comment.user.name, 'comment': comment.comment} for comment in post.comments]
                           }
                          for post in user.posts]
        return posts_info

    def add_post(self,p_title,p_desc):
        with so.Session(bind=self.engine) as session:
            user = session.merge(self.current_user)
            post = Post(title=p_title, description=p_desc, user_id = user.id)
            session.add(post)
            session.commit()
        return post

    def like_post(self, user_name:str, post_title:str):
        with so.Session(bind=self.engine) as session:


            user = session.scalars(sa.select(User).where(User.name == user_name)).one_or_none()
            post = session.scalars(sa.select(Post).where(Post.title == post_title)).one_or_none()


            # post.liked_by_users.append(user)
            # user.liked_posts.append(post)

            liked_or_not = session.scalars(sa.select(likes_table))

            session.execute(likes_table.insert().values(user_id=user.id, post_id=post.id))
            session.commit()


            print(f'You liked "{post_title}"')


        return post

    def comment_on_post(self, post_title: str, target_user_name: str, comment_text: str):
        with so.Session(bind=self.engine) as session:
            target_user = session.scalars(sa.select(User).where(User.name == target_user_name)).one_or_none()
            post = session.scalars(sa.select(Post).where(Post.title == post_title, Post.user_id == target_user.id)).one_or_none()

            user = session.merge(self.current_user)
            comment = Comment(user_id=user.id, post_id=post.id, comment=comment_text)
            session.add(comment)
            session.commit()
            print(f'Commented on "{post_title}": {comment_text}')




class CLI:
    def __init__(self):
        self.controller = Controller()
        self.login()

    @staticmethod
    def show_title(title):
        print('\n' + title)
        print('-' * len(title) + '\n')

    def login(self):
        self.show_title('Login Screen')
        users = self.controller.get_user_names()
        menu_items= users + ['Create a new account','Exit']
        menu_choice = pyip.inputMenu(menu_items, prompt = 'Select user or create a new account\n', numbered = True)
        if menu_choice.lower() == 'create a new account':
            self.create_account()
        elif menu_choice.lower() == 'exit':
            print('Goodbye')
        else:
            user_name = menu_choice
            self.controller.set_current_user_from_name(user_name)
            self.user_home()

    def create_account(self,existing_users = None):
        self.show_title('Create Account Screen')
        print("Enter Account Details")
        user_name = pyip.inputStr("Username: ", blockRegexes=existing_users, strip = None)
        age = pyip.inputInt("Age: ", min = 0, max = 150, blank = True)
        gender = pyip.inputMenu(['male','female','other'], prompt = "Gender: ",blank = True)#
        nationality = pyip.inputStr("Nationality: ")
        self.controller.create_user(user_name, age, gender, nationality)
        self.login()

    def user_home(self):
        self.show_title(f'{self.controller.current_user.name} Home Screen')
        print(f'Name: {self.controller.current_user.name}')
        print(f'Age: {self.controller.current_user.age}')
        print(f'Gender: {self.controller.current_user.gender}')
        print(f'Nationality: {self.controller.current_user.nationality}')
        self.show_posts(self.controller.current_user.name)
        menu_items = {'Show posts from another user': self.show_posts,
                      'Logout': self.login,
                      'Create a post': self.create_post,
                      }
        menu_choice = pyip.inputMenu(list(menu_items.keys()),
                                     prompt = 'Select an action\n',
                                     numbered = True,
                                     )
        menu_items[menu_choice]()
        if menu_choice != 'Logout':
            self.user_home()

    def show_posts(self, user_name: str | None = None):
        if user_name is None:
            users = self.controller.get_user_names()
            menu_choice = pyip.inputMenu(users,
                                         prompt='Select a user\n',
                                         numbered=True,
                                         )
            user_name = menu_choice

        self.show_title(f"{user_name}'s Posts")
        posts = self.controller.get_posts(user_name)
        for post in posts:
            print(f'Title: {post["title"]}')
            print(f'Content: {post["description"]}')
            print(f'Likes: {post["number_likes"]}')
            print(f'Comments: ')
            if post["comments"]:
                for comment in post["comments"]:
                    print(f'  - {comment["user"]}: {comment["comment"]}')

            else:
                print("  --No Comments--")

            like_post = str(input("Like this post?(y/n): "))
            if like_post.lower() == 'y':
                self.controller.like_post(user_name, post["title"])
                print(f'Likes: {post["number_likes"]}')

            comment_post = str(input("Comment on this post?(y/n): "))
            if comment_post.lower()=='y':
                comment_text = str(input("Enter your comment: "))
                self.controller.comment_on_post(post["title"], user_name, comment_text)

        if not posts:
            print('  --No Posts--')






    def create_post(self,):
        post_title = str(input("Enter the post title: "))
        post_description = str(input("Enter the post description: "))
        self.controller.add_post(post_title, post_description)



if __name__ == '__main__':
    cli = CLI()
    controller = Controller()
