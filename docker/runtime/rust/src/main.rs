#![feature(plugin)]
#![plugin(rocket_codegen)]

extern crate rocket;

#[get("/")]
fn index() -> &'static str {
    "Hello, world!"
}

#[get("/healthz")]
fn healthz() -> &'static str {
    "OK"
}


fn main() {
    rocket::ignite().mount("/", routes![index, healthz]).launch();
}
