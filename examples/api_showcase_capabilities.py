from crapssim_api.http import get_capabilities, start_session


if __name__ == "__main__":
    print("== GET /capabilities ==")
    print(get_capabilities().body.decode())

    print("\n== POST /start_session ==")
    sample_spec = {"enabled_buylay": False, "seed": 42}
    print(start_session({"spec": sample_spec, "seed": 42}).body.decode())
