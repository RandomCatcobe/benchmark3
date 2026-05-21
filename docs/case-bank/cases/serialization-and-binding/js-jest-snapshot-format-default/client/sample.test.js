test("snapshot shape", () => {
  expect({ nested: { value: 1 }, text: "line\nbreak" }).toMatchSnapshot();
});
