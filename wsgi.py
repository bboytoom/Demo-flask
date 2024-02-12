from src import create_app

app = create_app()

if __name__ == '__main__':
    # Remove ssl_context='adhoc' when make we deploy and change for host='0.0.0.0'
    app.run(host='0.0.0.0')
