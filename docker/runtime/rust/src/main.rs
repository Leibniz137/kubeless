#![feature(plugin)]
#![plugin(rocket_codegen)]

extern crate rocket;

fn hello_world() -> &'static str {
    "Hello, world!"
}


#[get("/")]
fn index() -> &'static str {
    return hello_world()
}

#[get("/healthz")]
fn healthz() -> &'static str {
    "OK"
}


fn main() {
    rocket::ignite().mount("/", routes![index, healthz]).launch();
}
