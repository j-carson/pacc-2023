import httpx
from prefect import flow


@flow
def fetch_cat_fact():
    return httpx.get("https://catfact.ninja/fact?max_length=140").json()["fact"]


@flow
def fetch_dog_fact():
    return httpx.get(
        "https://dogapi.dog/api/v2/facts",
        headers={"accept": "application/json"},
    ).json()["data"][0]["attributes"]["body"]


@flow(log_prints=True)
def animal_facts():
    cat_fact = fetch_cat_fact()
    dog_fact = fetch_dog_fact()
    print(f"🐱: {cat_fact} \n🐶: {dog_fact}")


if __name__ == "__main__":
    dep1 = animal_facts.to_deployment(name="animal_facts_2")
    dep2 = fetch_cat_fact.to_deployment(name="fetch_cat_fact_2")
    dep3 = fetch_dog_fact.to_deployment(name="fetch_dog_fact_2")
    serve(dep1, dep2, dep3)
