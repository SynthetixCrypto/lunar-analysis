// Workspace-scoped MCP recovery. No installed configuration or target writes.
import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
const root = path.dirname(fileURLToPath(import.meta.url));
const launcher = 'C:/Users/Admin/AppData/Local/npm-cache/_npx/af752b90495482d7/node_modules/rea-agents/scripts/rea.mjs';
const require = createRequire(launcher);
const {Client} = require('@modelcontextprotocol/client');
const {StdioClientTransport} = require('@modelcontextprotocol/client/stdio');
const sleep = ms => new Promise(r => setTimeout(r, ms));
const queue = path.join(root, 'queue');
await fs.mkdir(queue, {recursive:true});
await fs.mkdir(path.join(root,'evidence'), {recursive:true});
if (process.argv[2] === 'serve') {
  const client = new Client({name:'astra-static-research',version:'1.0.0'});
  const transport = new StdioClientTransport({command:process.execPath,args:[launcher,'--mcp'],env:{...process.env,GHIDRA_INSTALL_DIR:'C:\\tools\\ghidra_12.1.4_PUBLIC',JAVA_HOME:'C:\\Program Files\\Microsoft\\jdk-21.0.10.7-hotspot'},stderr:'pipe'});
  await client.connect(transport);
  transport.stderr?.on('data', b=>fs.appendFile(path.join(root,'rea-stderr.log'),b));
  await fs.writeFile(path.join(root,'tools-catalog.json'),JSON.stringify(await client.listTools(),null,2));
  await fs.writeFile(path.join(root,'ready.json'),JSON.stringify({pid:process.pid,launcher,ghidra:'C:\\tools\\ghidra_12.1.4_PUBLIC'}));
  let stop=false;
  try {
    while(!stop) {
      const files=(await fs.readdir(queue)).filter(f=>f.endsWith('.request.json')).sort();
      for(const file of files) {
        const request=JSON.parse(await fs.readFile(path.join(queue,file),'utf8'));
        let results=[];
        for(const call of request.calls) {
          try {
            const response=await client.callTool({name:call.name,arguments:call.arguments??{}},undefined,{timeout:1800000});
            const output=path.join(root,'evidence',`${call.id}.json`);
            await fs.writeFile(output,JSON.stringify(response,null,2));
            results.push({id:call.id,path:output,isError:response.isError??false});
          } catch(e) {results.push({id:call.id,error:String(e)});}
        }
        await fs.writeFile(path.join(queue,file.replace('.request.json','.response.json')),JSON.stringify(results,null,2));
        await fs.rename(path.join(queue,file),path.join(queue,file.replace('.request.json','.done.json')));
        stop ||= request.stop===true;
      }
      if(!stop) await sleep(200);
    }
  } finally {await client.close();}
} else if(process.argv[2] === 'request') {
  const input=process.argv[3];
  const id=`${Date.now()}`;
  const file=path.join(queue,`${id}.request.json`);
  await fs.writeFile(file,await fs.readFile(input));
  const response=file.replace('.request.json','.response.json');
  for(let n=0;n<9000;n++) {
    try { console.log(await fs.readFile(response,'utf8')); process.exit(0); } catch(e) {if(e.code!=='ENOENT') throw e;}
    await sleep(200);
  }
  throw Error('Request wait exceeded; inspect evidence and server log before retrying.');
}
