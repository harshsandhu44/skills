import { Command } from "commander";
import { registerList } from "./commands/list.js";
import { registerAdd } from "./commands/add.js";
import { registerSearch } from "./commands/search.js";

const program = new Command();

program
  .name("claude-skills")
  .description("Install Claude Code skills from the community skills library")
  .version("0.1.0");

registerList(program);
registerAdd(program);
registerSearch(program);

program.parse();
