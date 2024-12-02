from src.models import User


def seed_users(db):
    db.session.add_all([
        User(
            uuid='9bd82d2d-647f-4896-81ce-8055da610451', name='q9468v+obMmy06Awb7RZzg==',
            last_name='cknDFSGF1hofa4S3fpAOfw==', birth_day='26j+Ez8Tl8TUaWJAWYgHMg==', status=1,
            email='bgKCETfi8wXTNxfhKh7sHNcHoTLbNhHxwiJauwzoQQE=', deleted_at=None,
            password_hash='$2b$14$BMuyfjTZPui.zgx5fQQhG.bQuUMl2qqXZaM3NJnWXRtHsi250qjkG',
            created_at='2024-12-01 21:46:56', updated_at='2024-12-01 21:46:56'),
        User(
            uuid='90b4f3b1-6fe2-4c6c-b0de-f56e0b6dd677', name='6wPNeEsuRvmwYZCxYepbYQ==',
            last_name='dw69az1kC2xQFSaMNrMRfA==', birth_day='02/wMnRM5y7Zj3EG8LTfKw==', status=1,
            email='CiK5XlfLWKezYVCD6kHQfQ==', deleted_at=None,
            password_hash='$2b$14$zZUrbQYQidav0PGROC4x4ui3aTCNNQ7OSd2qXn3t/iifsYkrp1k5a',
            created_at='2024-12-01 21:46:56', updated_at='2024-12-01 21:46:56')
        ])

    db.session.commit()
