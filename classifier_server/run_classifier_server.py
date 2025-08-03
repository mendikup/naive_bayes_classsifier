import uvicorn

if __name__ == "__main__":
    # uvicorn.run("app_server.app_server:app_server", host="0.0.0.0", port=8080, reload=True)  # for Dockerfile
    uvicorn.run("app_server.app:app", host="127.0.0.1", port=8080, reload=True)

