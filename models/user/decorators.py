import functools
from typing import Callable
from flask import flash, redirect, session, url_for, current_app


def requires_login(func: Callable) -> Callable:

    @functools.wraps(func)
    def decorated_function(*args, **kwargs):
        if not session.get('email'):
            flash('You need to be signed in to display this page', 'danger')
            return redirect(url_for('users.login'))
        return func(*args, **kwargs)

    return decorated_function


def requires_admin(func: Callable) -> Callable:

    @functools.wraps(func)
    def decorated_function(*args, **kwargs):
        if not session.get('email') == current_app.config.get('ADMIN', '') is None:
            flash('You need to be an administrator in to access this page', 'danger')
            return redirect(url_for('users.login'))
        return func(*args, **kwargs)

    return decorated_function
