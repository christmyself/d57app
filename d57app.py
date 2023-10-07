import os
from app import create_app, db
from app.models import User, Role
from flask_migrate import Migrate,upgrade

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # 把数据库迁移到最新修订版本
    upgrade()
'''
    # 创建或更新用户角色
    Role.insert_roles()

    # 确保所有用户都关注了他们自己
    User.add_self_follows()
'''