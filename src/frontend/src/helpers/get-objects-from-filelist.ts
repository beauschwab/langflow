import { parse as parseYaml } from "yaml";

export async function getObjectsFromFilelist<T>(files: File[]): Promise<T[]> {
  let objects: T[] = [];
  for (const file of files) {
    const text = await file.text();
    const fileExtension = file.name.split(".").pop()?.toLowerCase();
    const isYamlFile = fileExtension === "yaml" || fileExtension === "yml";
    const fileData = isYamlFile ? parseYaml(text) : JSON.parse(text);
    objects.push(fileData as T);
  }
  return objects;
}
