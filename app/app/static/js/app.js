//console.log("Hello from app.js!");

$("#image").change(function() {
  filename = this.files[0].name
  console.log(filename);
});