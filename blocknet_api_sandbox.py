from __future__ import print_function
import time
import os
import json
import requests
import sys
import datetime
import asyncio
import discord
from discord.ext import commands

# RPCHost to Local Blocknet Wallet
class RPCHost(object):
    def __init__(self, url):
        self._session = requests.Session()
        self._url = url
        self._headers = {'content-type': 'application/json'}
    def call(self, rpcMethod, *params):
        payload = json.dumps({"method": rpcMethod, "params": list(params), "jsonrpc": "2.0"})
        tries = 5
        hadConnectionFailures = False
        while True:
            try:
                response = self._session.post(self._url, headers=self._headers, data=payload)
            except requests.exceptions.ConnectionError:
                tries -= 1
                if tries == 0:
                    raise Exception('Failed to connect for remote procedure call.')
                hadFailedConnections = True
                print("Couldn't connect for remote procedure call, will sleep for five seconds and then try again ({} more tries)".format(tries))
                time.sleep(10)
            else:
                if hadConnectionFailures:
                    print('Connected for remote procedure call after retry.')
                break
        if not response.status_code in (200, 500):
            raise Exception('RPC connection failure: ' + str(response.status_code) + ' ' + response.reason)
        responseJSON = response.json()
        if 'error' in responseJSON and responseJSON['error'] != None:
            raise Exception('Error in RPC call: ' + str(responseJSON['error']))
        return responseJSON['result']

# The port number depends on the one writte in the blocknetdx.conf file
rpcPort = 41414
# The RPC username and RPC password MUST match the one in your blocknetdx.conf file
rpcUser = 'block'
rpcPassword = 'block123'

# Accessing the RPC local server
serverURL = 'http://' + rpcUser + ':' + rpcPassword + '@localhost:' + str(rpcPort)

######

# Discord Bot
client = commands.Bot(command_prefix = '!')

# Output when Bot is online and ready to use
@client.event
async def on_ready():
	print('Bot is ready.')
	print('Logged in as:')
	print(client.user.name)
	print(client.user.id)
	print('------')

# Error Handling
@client.event
async def on_command_error(ctx, error):

	if isinstance(error, commands.errors.MissingRequiredArgument):
		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0xff0000)

		embed.set_author(name="API Error", icon_url="https://pbs.twimg.com/profile_images/969254471636103168/gMHQ6_-5_400x400.jpg")
		embed.add_field(name="Parameter Error:", value='`%s`' % error, inline=False)
		embed.add_field(name="Solution:", value="Verify API usage by viewing !XRouter or !XCloud", inline=False)
		embed.set_footer(text="API Error Timestamp")

		await ctx.send(embed=embed)
		return

	if isinstance(error, commands.errors.CommandNotFound):
		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0xff0000)

		embed.set_author(name="BOT Error", icon_url="https://pbs.twimg.com/profile_images/969254471636103168/gMHQ6_-5_400x400.jpg")
		embed.add_field(name="Command Error:", value='`%s`' % error, inline=False)
		embed.add_field(name="Solution:", value="Search available commands by typing !help", inline=False)
		embed.set_footer(text="BOT Error Timestamp")

		await ctx.send(embed=embed)
		return

	if isinstance(error, commands.errors.CommandInvokeError):
		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0xff0000)

		embed.set_author(name="BOT Error", icon_url="https://pbs.twimg.com/profile_images/969254471636103168/gMHQ6_-5_400x400.jpg")
		embed.add_field(name="Error:", value='`%s`' % error, inline=False)
		embed.add_field(name="Solution:", value="Retry call, if problem persists contact the Blocknet Core Team", inline=False)
		embed.set_footer(text="BOT Error Timestamp")

		await ctx.send(embed=embed)
		return		

# !info command
@client.command()
async def info(ctx):
    embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x142c46)
    
    embed.set_author(name="Information", icon_url="https://pbs.twimg.com/profile_images/969254471636103168/gMHQ6_-5_400x400.jpg")
    embed.add_field(name="Purpose", value="> Blocknet API Bot provides a quick API sandbox experience right in Discord without needing the Blocknet client", inline=False)
    embed.add_field(name="Links", value="> [Blocknet Website](https://blocknet.co/) \n > [API](https://api.blocknet.co/) \n > [Documentation](https://docs.blocknet.co/) \n > [Forum](https://forum.blocknet.co/) \n > [Github](https://github.com/BlocknetDX)", inline=False)
    embed.add_field(name="Notes", value="> * All commands begin with ! \n > * Due to character limitations with Discord, large API responses will output to a JSON file \n > * Type !help to view available commands", inline=False)
    embed.set_footer(text="Blocknet API Bot Info")

    await ctx.send(embed=embed)

# !help command
client.remove_command('help')

@client.command()
async def help(ctx):
    embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x142c46)

    embed.set_author(name="Available Commands", icon_url="https://pbs.twimg.com/profile_images/969254471636103168/gMHQ6_-5_400x400.jpg")
    embed.add_field(name="!help", value="> Lists available Blocknet API Bot commands", inline=False)
    embed.add_field(name="!info", value="> Information about the Blocknet API Bot", inline=False)
    embed.add_field(name="!XRouter", value="> Lists available XRouter API commands", inline=False)
    embed.add_field(name="!XCloud", value="> Lists available XCloud API commands", inline=False)
    embed.set_footer(text="Blocknet API Bot Help")

    await ctx.send(embed=embed)

# !XRouter command
@client.command()
async def XRouter(ctx):
    embed = discord.Embed(title="Available XRouter Commands:", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8)

    embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
    embed.add_field(name="xrGetNetworkServices", value="> **Description:** Returns supported XRouter services \n > **Usage:** `!xrGetNetworkServices` \n > **Link:** [xrGetNetworkServices](https://api.blocknet.co/#xrgetnetworkservices)", inline=False)
    embed.add_field(name="xrConnect", value="> **Description:** Pre-connect to XRouter nodes \n > **Usage:** `!xrConnect [service] [node_count]` \n > **Link:** [xrConnect](https://api.blocknet.co/#xrconnect)", inline=False)
    embed.add_field(name="xrConnectedNodes", value="> **Description:** Returns connected node services and fees \n > **Usage:** `!xrConnectedNodes` \n > **Link:** [xrConnectedNodes](https://api.blocknet.co/#xrconnectednodes)", inline=False)
    embed.add_field(name="xrGetBlockCount", value="> **Description:** Returns a blockchain's block height \n > **Usage:** `!xrGetBlockCount [blockchain] [node_count]` \n > **Link:** [xrGetBlockCount](https://api.blocknet.co/#xrgetblockcount)", inline=False)
    embed.add_field(name="xrGetBlockHash", value="> **Description:** Returns a block number's hash \n > **Usage:** `!xrGetBlockHash [blockchain] [block_number] [node_count]` \n > **Link:** [xrGetBlockHash](https://api.blocknet.co/#xrgetblockhash)", inline=False)
    embed.add_field(name="xrGetBlock", value="> **Description:** Returns a block hash's block number \n > **Usage:** `!xrGetBlock [blockchain] [block_hash] [node_count]` \n > **Link:** [xrGetBlock](https://api.blocknet.co/#xrgetblock)", inline=False)
    embed.add_field(name="xrGetBlocks", value="> **Description:** Returns block hashes for multiple block numbers \n > **Usage:** `!xrGetBlocks [blockchain] [block_hash1,block_hash2,block_hashN] [node_count]` \n > **Link:** [xrGetBlocks](https://api.blocknet.co/#xrgetblocks)", inline=False)
    embed.add_field(name="xrDecodeRawTransaction", value="> **Description:** Returns decoded transaction HEX \n > **Usage:** `!xrDecodeRawTransaction [blockchain] [tx_hex] [node_count]` \n > **Link:** [xrDecodeRawTransaction](https://api.blocknet.co/#xrdecoderawtransaction)", inline=False)
    embed.add_field(name="xrGetTransaction", value="> **Description:** Returns transaction data for transaction ID \n > **Usage:** `!xrGetTransaction [blockchain] [txid] [node_count]` \n > **Link:** [xrGetTransaction](https://api.blocknet.co/#xrgettransaction)", inline=False)
    embed.add_field(name="xrGetTransactions", value="> **Description:** Returns transaction data for multiple transaction IDs \n > **Usage:** `!xrGetTransactions [blockchain] [txid1,txid2,txidN] [node_count]` \n > **Link:** [xrGetTransactions](https://api.blocknet.co/#xrgettransactions)", inline=False)
    embed.add_field(name="xrSendTransaction", value="> **Description:** Submit a signed transaction to the network \n > **Usage:** `!xrSendTransaction [blockchain] [signed_tx]` \n > **Link:** [xrSendTransaction](https://api.blocknet.co/#xrsendtransaction)", inline=False)
    embed.add_field(name="xrGetReply", value="> **Description:** Returns prior response associated with UUID \n > **Usage:** `!xrGetReply [uuid]` \n > **Link:** [xrGetReply](https://api.blocknet.co/#xrgetreply)", inline=False)
    embed.add_field(name="xrShowConfigs", value="> **Description:** Returns all node configs received as raw text \n > **Usage:** `!xrShowConfigs` \n > **Link:** [xrShowConfigs](https://api.blocknet.co/#xrshowconfigs)", inline=False)
    embed.add_field(name="xrReloadConfigs", value="> **Description:** Applies changes made to your configs \n > **Usage:** `!xrReloadConfigs` \n > **Link:** [xrReloadConfigs](https://api.blocknet.co/#xrreloadconfigs)", inline=False)
    embed.add_field(name="xrStatus", value="> **Description:** Returns your XRouter configurations \n > **Usage:** `!xrStatus` \n > **Link:** [xrStatus](https://api.blocknet.co/#xrstatus)", inline=False)
    embed.set_footer(text="XRouter API")

    await ctx.send(embed=embed)

# !XCloud command
@client.command()
async def XCloud(ctx):
    embed = discord.Embed(title="Available XCloud Commands:", description="", timestamp=datetime.datetime.utcnow(), color=0xf67d72)

    embed.set_author(name="XCloud API", icon_url="https://pbs.twimg.com/profile_images/1151998583052177408/eJhAuafL_400x400.jpg")
    embed.add_field(name="xrService", value="> **Description:** Use to interact with XCloud services \n > **Usage:** `!xrService [service] [param1] [param2] [paramN]` \n > **Link:** [xrService](https://api.blocknet.co/#xrservice)", inline=False)
    embed.add_field(name="xrServiceConsensus", value="> ** Description:** Use to interact with XCloud services with consensus \n > **Usage:** `!xrServiceConsensus [node_count] [service] [param1] [param2] [paramN]` \n > **Link:** [xrServiceConsensus](https://api.blocknet.co/#xrserviceconsensus)", inline=False)
    embed.set_footer(text="XCloud API")

    await ctx.send(embed=embed)

# XCloud embed

# !xrService
@client.command()
async def xrService(ctx, arg1, *argv):
	host = RPCHost(serverURL)
	xrService = host.call('xrService', arg1, *argv)
	xrService_JSON = "```" + json.dumps(xrService, sort_keys=False, indent=4) + "```"
	xrService_RAW = json.dumps(xrService)

	xcloudLengthErr = "API response too long, see attached file for full response.\n\nTruncated API response preview: "
	truncateLength = 1000 - len(xcloudLengthErr)
	response = "```" + xcloudLengthErr + "```" + xrService_JSON[:truncateLength] + "\n..."+ "```"

	if len(xrService_RAW) > 500:

		with open('xrService '+ arg1 + '.json', 'w') as fp:
			json.dump(xrService, fp, sort_keys=False, indent=4)
		file = discord.File('xrService '+ arg1 + '.json', filename='xrService '+ arg1 + '.json')

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0xf67d72) 
		
		embed.set_author(name="XCloud API", icon_url="https://pbs.twimg.com/profile_images/1151998583052177408/eJhAuafL_400x400.jpg")
		embed.add_field(name="Command:", value="`xrService " + arg1 + " `", inline=False)
		embed.add_field(name="Response:", value=response, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(file=file, embed=embed)
		os.remove('xrService '+ arg1 + '.json')

	else:

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0xf67d72) 

		embed.set_author(name="XCloud API", icon_url="https://pbs.twimg.com/profile_images/1151998583052177408/eJhAuafL_400x400.jpg")
		embed.add_field(name="Command:", value="`xrService " + arg1 + " `", inline=False)
		embed.add_field(name="Response:", value=xrService_JSON, inline=False)
		embed.set_footer(text="API Response Timestamp")
	
		await ctx.send(embed=embed)

# !xrServiceConsensus
@client.command()
async def xrServiceConsensus(ctx, arg1, arg2, *argv):
	host = RPCHost(serverURL)
	xrServiceConsensus = host.call('xrServiceConsensus', int(arg1), arg2, *argv)
	xrServiceConsensus_JSON = "```" + json.dumps(xrServiceConsensus, sort_keys=False, indent=4) + "```"
	xrServiceConsensus_RAW = json.dumps(xrServiceConsensus)

	xcloudLengthErr = "API response too long, see attached file for full response.\n\nTruncated API response preview: "
	truncateLength = 1000 - len(xcloudLengthErr)
	response = "```" + xcloudLengthErr + "```" + xrServiceConsensus_JSON[:truncateLength] + "\n..."+ "```"

	if len(xrServiceConsensus_RAW) > 500:

		with open('xrServiceConsensus '+ arg1 + ' ' + arg2 + '.json', 'w') as fp:
			json.dump(xrServiceConsensus, fp, sort_keys=False, indent=4)
		file = discord.File('xrServiceConsensus '+ arg1 + ' ' + arg2 + '.json', filename='xrServiceConsensus '+ arg1 + ' ' + arg2 + '.json')

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0xf67d72) 

		embed.set_author(name="XCloud API", icon_url="https://pbs.twimg.com/profile_images/1151998583052177408/eJhAuafL_400x400.jpg")
		embed.add_field(name="Command:", value="`xrServiceConsensus " + arg1 + ' ' + arg2 + " `", inline=False)
		embed.add_field(name="Response:", value=response, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(file=file, embed=embed)
		os.remove('xrServiceConsensus '+ arg1 + ' ' + arg2 + '.json')	

	else:

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0xf67d72) 

		embed.set_author(name="XCloud API", icon_url="https://pbs.twimg.com/profile_images/1151998583052177408/eJhAuafL_400x400.jpg")
		embed.add_field(name="Command:", value="`xrServiceConsensus " + arg1 + ' ' + arg2 + " `", inline=False)
		embed.add_field(name="Response:", value=xrServiceConsensus_JSON, inline=False)
		embed.set_footer(text="API Response Timestamp")
	
		await ctx.send(embed=embed)

# XRouter embed

# !xrGetNetworkServices
@client.command()
async def xrGetNetworkServices(ctx):
	host = RPCHost(serverURL)
	xrGetNetworkServices = host.call('xrGetNetworkServices')
	xrGetNetworkServices_JSON = "```" + json.dumps(xrGetNetworkServices, sort_keys=False, indent=4) + "```"
	xrGetNetworkServices_RAW = json.dumps(xrGetNetworkServices)

	xcloudLengthErr = "API response too long, see attached file for full response.\n\nTruncated API response preview: "
	truncateLength = 1000 - len(xcloudLengthErr)
	response = "```" + xcloudLengthErr + "```" + xrGetNetworkServices_JSON[:truncateLength] + "\n..."+ "```"

	if len(xrGetNetworkServices_RAW) > 1000:

		with open('xrGetNetworkServices.json', 'w') as fp:
			json.dump(xrGetNetworkServices, fp, sort_keys=False, indent=4)
		file = discord.File("xrGetNetworkServices.json", filename="xrGetNetworkServices.json")

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8)

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrGetNetworkServices" + "`", inline=False)
		embed.add_field(name="Response:", value=response, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(file=file, embed=embed)
		os.remove("xrGetNetworkServices.json")

	else:

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8) 

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrGetNetworkServices" + "`", inline=False)
		embed.add_field(name="Response:", value=xrGetNetworkServices_JSON, inline=False)
		embed.set_footer(text="API Response Timestamp")
	
		await ctx.send(embed=embed)

# !xrGetBlockCount
@client.command()
async def xrGetBlockCount(ctx, arg1, arg2):
	host = RPCHost(serverURL)
	xrGetBlockCount = host.call('xrGetBlockCount', arg1, int(arg2))
	xrGetBlockCount_JSON = "```" + json.dumps(xrGetBlockCount, sort_keys=False, indent=4) + "```"
	xrGetBlockCount_RAW = json.dumps(xrGetBlockCount)

	xcloudLengthErr = "API response too long, see attached file for full response.\n\nTruncated API response preview: "
	truncateLength = 1000 - len(xcloudLengthErr)
	response = "```" + xcloudLengthErr + "```" + xrGetBlockCount_JSON[:truncateLength] + "\n..."+ "```"

	if len(xrGetBlockCount_RAW) > 1000:

		with open('xrGetBlockCount '+ arg1 + ' ' + arg2 + '.json', 'w') as fp:
			json.dump(xrGetBlockCount, fp, sort_keys=False, indent=4)
		file = discord.File('xrGetBlockCount '+ arg1 + ' ' + arg2 + '.json', filename='xrGetBlockCount '+ arg1 + ' ' + arg2 + '.json')

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8)

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrGetBlockCount " + arg1 + ' ' + arg2 +"`", inline=False)
		embed.add_field(name="Response:", value=response, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(file=file, embed=embed)
		os.remove('xrGetBlockCount '+ arg1 + ' ' + arg2 + '.json')

	else:

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8) 

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrGetBlockCount " + arg1 + ' ' + arg2 +"`", inline=False)
		embed.add_field(name="Response:", value=xrGetBlockCount_JSON, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(embed=embed)

# !xrGetBlockHash
@client.command()
async def xrGetBlockHash(ctx, arg1, arg2, arg3):
	host = RPCHost(serverURL)
	xrGetBlockHash = host.call('xrGetBlockHash', arg1, arg2, int(arg3))
	xrGetBlockHash_JSON = "```" + json.dumps(xrGetBlockHash, sort_keys=False, indent=4) + "```"
	xrGetBlockHash_RAW = json.dumps(xrGetBlockHash)

	xcloudLengthErr = "API response too long, see attached file for full response.\n\nTruncated API response preview: "
	truncateLength = 1000 - len(xcloudLengthErr)
	response = "```" + xcloudLengthErr + "```" + xrGetBlockHash_JSON[:truncateLength] + "\n..."+ "```"

	if len(xrGetBlockHash_RAW) > 1000:

		with open('xrGetBlockHash '+ arg1 + ' ' + arg2 + ' ' + arg3  + '.json', 'w') as fp:
			json.dump(xrGetBlockHash, fp, sort_keys=False, indent=4)
		file = discord.File('xrGetBlockHash '+ arg1 + ' ' + arg2 + ' ' + arg3  + '.json', filename='xrGetBlockHash '+ arg1 + ' ' + arg2 + ' ' + arg3  + '.json')

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8)

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrGetBlockHash " + arg1 + ' ' + arg2 + ' ' + arg3  + "`", inline=False)
		embed.add_field(name="Response:", value=response, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(file=file, embed=embed)
		os.remove('xrGetBlockHash '+ arg1 + ' ' + arg2 + ' ' + arg3  + '.json')

	else:

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8) 

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrGetBlockHash " + arg1 + ' ' + arg2 + ' ' + arg3  + "`", inline=False)
		embed.add_field(name="Response:", value=xrGetBlockHash_JSON, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(embed=embed)

# !xrGetBlock
@client.command()
async def xrGetBlock(ctx, arg1, arg2, arg3):
	host = RPCHost(serverURL)
	xrGetBlock = host.call('xrGetBlock', arg1, arg2, int(arg3))
	xrGetBlock_JSON = "```" + json.dumps(xrGetBlock, sort_keys=False, indent=4) + "```"
	xrGetBlock_RAW = json.dumps(xrGetBlock)

	xcloudLengthErr = "API response too long, see attached file for full response.\n\nTruncated API response preview: "
	truncateLength = 1000 - len(xcloudLengthErr)
	response = "```" + xcloudLengthErr + "```" + xrGetBlock_JSON[:truncateLength] + "\n..."+ "```"

	if len(xrGetBlock_RAW) > 1000:

		with open('xrGetBlock '+ arg1 + ' ' + arg2 + ' ' + arg3 + '.json', 'w') as fp:
			json.dump(xrGetBlock, fp, sort_keys=False, indent=4)
		file = discord.File('xrGetBlock '+ arg1 + ' ' + arg2 + ' ' + arg3 + '.json', filename='xrGetBlock '+ arg1 + ' ' + arg2 + ' ' + arg3 + '.json')

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8) 

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrGetBlock " + arg1 + ' ' + arg2 + ' ' + arg3 +"`", inline=False)
		embed.add_field(name="Response:", value=response, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(file=file, embed=embed)
		os.remove('xrGetBlock '+ arg1 + ' ' + arg2 + ' ' + arg3 + '.json')

	else:

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8) 

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrGetBlock " + arg1 + ' ' + arg2 + ' ' + arg3 +"`", inline=False)
		embed.add_field(name="Response:", value=xrGetBlock_JSON, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(embed=embed)

# !xrGetBlocks
@client.command()
async def xrGetBlocks(ctx, arg1, arg2, arg3):
	host = RPCHost(serverURL)
	xrGetBlocks = host.call('xrGetBlocks', arg1, arg2, int(arg3))
	xrGetBlocks_JSON = "```" + json.dumps(xrGetBlocks, sort_keys=False, indent=4) + "```"
	xrGetBlocks_RAW = json.dumps(xrGetBlocks)

	xcloudLengthErr = "API response too long, see attached file for full response.\n\nTruncated API response preview: "
	truncateLength = 1000 - len(xcloudLengthErr)
	response = "```" + xcloudLengthErr + "```" + xrGetBlocks_JSON[:truncateLength] + "\n..."+ "```"

	if len(xrGetBlocks_RAW) > 1000:

		with open('xrGetBlocks '+ arg1 + ' ' + arg2 + ' ' + arg3 + '.json', 'w') as fp:
			json.dump(xrGetBlocks, fp, sort_keys=False, indent=4)
		file = discord.File('xrGetBlocks '+ arg1 + ' ' + arg2 + ' ' + arg3 + '.json', filename='xrGetBlocks '+ arg1 + ' ' + arg2 + ' ' + arg3 + '.json')	

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8) 

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrGetBlocks " + arg1 + ' ' + arg2 + ' ' + arg3 +"`", inline=False)
		embed.add_field(name="Response:", value=response, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(file=file, embed=embed)
		os.remove('xrGetBlocks '+ arg1 + ' ' + arg2 + ' ' + arg3 + '.json')

	else:

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8) 

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrGetBlocks " + arg1 + ' ' + arg2 + ' ' + arg3 +"`", inline=False)
		embed.add_field(name="Response:", value=xrGetBlocks_JSON, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(embed=embed)

# !xrGetTransaction
@client.command()
async def xrGetTransaction(ctx, arg1, arg2, arg3):
	host = RPCHost(serverURL)
	xrGetTransaction = host.call('xrGetTransaction', arg1, arg2, int(arg3))
	xrGetTransaction_JSON = "```" + json.dumps(xrGetTransaction, sort_keys=False, indent=4) + "```"
	xrGetTransaction_RAW = json.dumps(xrGetTransaction)

	xcloudLengthErr = "API response too long, see attached file for full response.\n\nTruncated API response preview: "
	truncateLength = 1000 - len(xcloudLengthErr)
	response = "```" + xcloudLengthErr + "```" + xrGetTransaction_JSON[:truncateLength] + "\n..."+ "```"

	if len(xrGetTransaction_RAW) > 1000:

		with open('xrGetTransaction '+ arg1 + ' ' + arg2 + ' ' + arg3 + '.json', 'w') as fp:
			json.dump(xrGetTransaction, fp, sort_keys=False, indent=4)
		file = discord.File('xrGetTransaction '+ arg1 + ' ' + arg2 + ' ' + arg3 + '.json', filename='xrGetTransaction '+ arg1 + ' ' + arg2 + ' ' + arg3 + '.json')

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8) 

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrGetTransaction " + arg1 + ' ' + arg2 + ' ' + arg3 +"`", inline=False)
		embed.add_field(name="Response:", value=response, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(file=file, embed=embed)
		os.remove('xrGetTransaction '+ arg1 + ' ' + arg2 + ' ' + arg3 + '.json')

	else:

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8) 

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrGetTransaction " + arg1 + ' ' + arg2 + ' ' + arg3 +"`", inline=False)
		embed.add_field(name="Response:", value=xrGetTransaction_JSON, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(embed=embed)

# !xrGetTransactions
@client.command()
async def xrGetTransactions(ctx, arg1, arg2, arg3):
	host = RPCHost(serverURL)
	xrGetTransactions = host.call('xrGetTransactions', arg1, arg2, int(arg3))
	xrGetTransactions_JSON = "```" + json.dumps(xrGetTransactions, sort_keys=False, indent=4) + "```"
	xrGetTransactions_RAW = json.dumps(xrGetTransactions)

	xcloudLengthErr = "API response too long, see attached file for full response.\n\nTruncated API response preview: "
	truncateLength = 1000 - len(xcloudLengthErr)
	response = "```" + xcloudLengthErr + "```" + xrGetTransactions_JSON[:truncateLength] + "\n..."+ "```"

	if len(xrGetTransactions_RAW) > 1000:

		with open('xrGetTransactions '+ arg1 + ' ' + arg2 + ' ' + arg3 + '.json', 'w') as fp:
			json.dump(xrGetTransactions, fp, sort_keys=False, indent=4)
		file = discord.File('xrGetTransactions '+ arg1 + ' ' + arg2 + ' ' + arg3 + '.json', filename='xrGetTransactions '+ arg1 + ' ' + arg2 + ' ' + arg3 + '.json')

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8) 

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrGetTransactions " + arg1 + ' ' + arg2 + ' ' + arg3 +"`", inline=False)
		embed.add_field(name="Response:", value=response, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(file=file, embed=embed)
		os.remove('xrGetTransactions '+ arg1 + ' ' + arg2 + ' ' + arg3 + '.json')

	else:

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8) 

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrGetTransactions " + arg1 + ' ' + arg2 + ' ' + arg3 +"`", inline=False)
		embed.add_field(name="Response:", value=xrGetTransactions_JSON, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(embed=embed)

# !xrConnectedNodes
@client.command()
async def xrConnectedNodes(ctx):
	host = RPCHost(serverURL)
	xrConnectedNodes = host.call('xrConnectedNodes')
	xrConnectedNodes_JSON = "```" + json.dumps(xrConnectedNodes, sort_keys=False, indent=4) + "```"
	xrConnectedNodes_RAW = json.dumps(xrConnectedNodes)

	xcloudLengthErr = "API response too long, see attached file for full response.\n\nTruncated API response preview: "
	truncateLength = 1000 - len(xcloudLengthErr)
	response = "```" + xcloudLengthErr + "```" + xrConnectedNodes_JSON[:truncateLength] + "\n..."+ "```"
	
	if len(xrConnectedNodes_RAW) > 1000:

		with open('xrConnectedNodes.json', 'w') as fp:
			json.dump(xrConnectedNodes, fp, sort_keys=False, indent=4)
		file = discord.File("xrConnectedNodes.json", filename="xrConnectedNodes.json")

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8)

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrConnectedNodes" + "`", inline=False)
		embed.add_field(name="Response:", value=response, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(file=file, embed=embed)
		os.remove("xrConnectedNodes.json")

	else:

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8) 

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrConnectedNodes" + "`", inline=False)
		embed.add_field(name="Response:", value=xrConnectedNodes_JSON, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(embed=embed)

# !xrConnect
@client.command()
async def xrConnect(ctx, arg1, arg2):
	host = RPCHost(serverURL)
	xrConnect = host.call('xrConnect', arg1, int(arg2))
	xrConnect_JSON = "```" + json.dumps(xrConnect, sort_keys=False, indent=4) + "```"
	xrConnect_RAW = json.dumps(xrConnect)

	xcloudLengthErr = "API response too long, see attached file for full response.\n\nTruncated API response preview: "
	truncateLength = 1000 - len(xcloudLengthErr)
	response = "```" + xcloudLengthErr + "```" + xrConnect_JSON[:truncateLength] + "\n..."+ "```"

	if len(xrConnect_RAW) > 1000:

		with open('xrConnect.json', 'w') as fp:
			json.dump(xrConnect, fp, sort_keys=False, indent=4)
		file = discord.File("xrConnect.json", filename="xrConnect.json")

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8) 

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrConnect " + arg1 + ' ' + arg2 +"`", inline=False)
		embed.add_field(name="Response:", value=response, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(file=file, embed=embed)
		os.remove("xrConnect.json")

	else:

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8) 

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrConnect " + arg1 + ' ' + arg2 +"`", inline=False)
		embed.add_field(name="Response:", value=xrConnect_JSON, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(embed=embed)

# !xrShowConfigs
@client.command()
async def xrShowConfigs(ctx):
	host = RPCHost(serverURL)
	xrShowConfigs = host.call('xrShowConfigs')
	xrShowConfigs_JSON = "```" + json.dumps(xrShowConfigs, sort_keys=False, indent=4) + "```"
	xrShowConfigs_RAW = json.dumps(xrShowConfigs)

	xcloudLengthErr = "API response too long, see attached file for full response.\n\nTruncated API response preview: "
	truncateLength = 1000 - len(xcloudLengthErr)
	response = "```" + xcloudLengthErr + "```" + xrShowConfigs_JSON[:truncateLength] + "\n..."+ "```"
	
	if len(xrShowConfigs_RAW) > 1000:

		with open('xrShowConfigs.json', 'w') as fp:
			json.dump(xrShowConfigs, fp, sort_keys=False, indent=4)
		file = discord.File("xrShowConfigs.json", filename="xrShowConfigs.json")

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8)

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrShowConfigs" + "`", inline=False)
		embed.add_field(name="Response:", value=response, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(file=file, embed=embed)
		os.remove("xrShowConfigs.json")

	else:

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8) 

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrShowConfigs" + "`", inline=False)
		embed.add_field(name="Response:", value=xrShowConfigs_JSON, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(embed=embed)

# !xrReloadConfigs
@client.command()
async def xrReloadConfigs(ctx):
	host = RPCHost(serverURL)
	xrReloadConfigs = host.call('xrReloadConfigs')
	xrReloadConfigs_JSON = "```" + json.dumps(xrReloadConfigs, sort_keys=False, indent=4) + "```"
	xrReloadConfigs_RAW = json.dumps(xrReloadConfigs)

	xcloudLengthErr = "API response too long, see attached file for full response.\n\nTruncated API response preview: "
	truncateLength = 1000 - len(xcloudLengthErr)
	response = "```" + xcloudLengthErr + "```" + xrReloadConfigs_JSON[:truncateLength] + "\n..."+ "```"
	
	if len(xrReloadConfigs_RAW) > 1000:

		with open('xrReloadConfigs.json', 'w') as fp:
			json.dump(xrReloadConfigs, fp, sort_keys=False, indent=4)
		file = discord.File("xrReloadConfigs.json", filename="xrReloadConfigs.json")

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8)

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrReloadConfigs" + "`", inline=False)
		embed.add_field(name="Response:", value=response, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(file=file, embed=embed)
		os.remove("xrReloadConfigs.json")

	else:

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8) 

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrReloadConfigs" + "`", inline=False)
		embed.add_field(name="Response:", value=xrReloadConfigs_JSON, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(embed=embed)

# !xrStatus
@client.command()
async def xrStatus(ctx):
	host = RPCHost(serverURL)
	xrStatus = host.call('xrStatus')
	xrStatus_JSON = "```" + json.dumps(xrStatus, sort_keys=False, indent=4) + "```"
	xrStatus_RAW = json.dumps(xrStatus)

	xcloudLengthErr = "API response too long, see attached file for full response.\n\nTruncated API response preview: "
	truncateLength = 1000 - len(xcloudLengthErr)
	response = "```" + xcloudLengthErr + "```" + xrStatus_JSON[:truncateLength] + "\n..."+ "```"
	
	if len(xrStatus_RAW) > 1000:

		with open('xrStatus.json', 'w') as fp:
			json.dump(xrStatus, fp, sort_keys=False, indent=4)
		file = discord.File("xrStatus.json", filename="xrStatus.json")

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8)

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrStatus" + "`", inline=False)
		embed.add_field(name="Response:", value=response, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(file=file, embed=embed)
		os.remove("xrStatus.json")

	else:

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8) 

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrStatus" + "`", inline=False)
		embed.add_field(name="Response:", value=xrStatus_JSON, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(embed=embed)

# !xrGetReply
@client.command()
async def xrGetReply(ctx, arg1):
	host = RPCHost(serverURL)
	xrGetReply = host.call('xrGetReply', arg1)
	xrGetReply_JSON = "```" + json.dumps(xrGetReply, sort_keys=False, indent=4) + "```"
	xrGetReply_RAW = json.dumps(xrGetReply)

	xcloudLengthErr = "API response too long, see attached file for full response.\n\nTruncated API response preview: "
	truncateLength = 1000 - len(xcloudLengthErr)
	response = "```" + xcloudLengthErr + "```" + xrGetReply_JSON[:truncateLength] + "\n..."+ "```"
	
	if len(xrGetReply_RAW) > 1000:

		with open('xrGetReply '+ arg1 + '.json', 'w') as fp:
			json.dump(xrGetReply, fp, sort_keys=False, indent=4)
		file = discord.File('xrGetReply '+ arg1 + '.json', filename='xrGetReply '+ arg1 + '.json')

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8)

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrGetReply " + arg1 + "`", inline=False)
		embed.add_field(name="Response:", value=response, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(file=file, embed=embed)
		os.remove('xrGetReply '+ arg1 + '.json')

	else:

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8) 

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrGetReply " + arg1 + "`", inline=False)
		embed.add_field(name="Response:", value=xrGetReply_JSON, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(embed=embed)

# !xrSendTransaction
@client.command()
async def xrSendTransaction(ctx, arg1, arg2):
	host = RPCHost(serverURL)
	xrSendTransaction = host.call('xrSendTransaction', arg1, arg2)
	xrSendTransaction_JSON = "```" + json.dumps(xrSendTransaction, sort_keys=False, indent=2) + "```"
	xrSendTransaction_RAW = json.dumps(xrSendTransaction)

	xcloudLengthErr = "API response too long, see attached file for full response.\n\nTruncated API response preview: "
	truncateLength = 1000 - len(xcloudLengthErr)
	response = "```" + xcloudLengthErr + "```" + xrSendTransaction_JSON[:truncateLength] + "\n..."+ "```"

	if len(xrSendTransaction_RAW) > 1000:

		with open('xrSendTransaction '+ arg1 + ' ' + arg2 + '.json', 'w') as fp:
			json.dump(xrSendTransaction, fp, sort_keys=False, indent=4)
		file = discord.File('xrSendTransaction '+ arg1 + ' ' + arg2 + '.json', filename='xrSendTransaction '+ arg1 + ' ' + arg2 + '.json')

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8)

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrSendTransaction " + arg1 + ' ' + "[signed_tx]" +"`", inline=False)
		embed.add_field(name="Response:", value=response, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(file=file, embed=embed)
		os.remove('xrSendTransaction '+ arg1 + ' ' + arg2 + '.json')

	else:

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8) 

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrSendTransaction " + arg1 + ' ' + "[signed_tx]" +"`", inline=False)
		embed.add_field(name="Response:", value=xrSendTransaction_JSON, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(embed=embed)

# !xrDecodeRawTransaction
@client.command()
async def xrDecodeRawTransaction(ctx, arg1, arg2, arg3):
	host = RPCHost(serverURL)
	xrDecodeRawTransaction = host.call('xrDecodeRawTransaction', arg1, arg2, int(arg3))
	xrDecodeRawTransaction_JSON = "```" + json.dumps(xrDecodeRawTransaction, sort_keys=False, indent=4) + "```"
	xrDecodeRawTransaction_RAW = json.dumps(xrDecodeRawTransaction)

	xcloudLengthErr = "API response too long, see attached file for full response.\n\nTruncated API response preview: "
	truncateLength = 1000 - len(xcloudLengthErr)
	response = "```" + xcloudLengthErr + "```" + xrDecodeRawTransaction_JSON[:truncateLength] + "\n..."+ "```"

	if len(xrDecodeRawTransaction_RAW) > 1000:

		with open('xrDecodeRawTransaction '+ arg1 + ' ' + '[tx_hex]' + ' ' + arg3 + '.json', 'w') as fp:
			json.dump(xrDecodeRawTransaction, fp, sort_keys=False, indent=4)
		file = discord.File('xrDecodeRawTransaction '+ arg1 + ' ' + '[tx_hex]' + ' ' + arg3 + '.json', filename='xrDecodeRawTransaction '+ arg1 + ' ' + '[tx_hex]' + ' ' + arg3 + '.json')

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8) 

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrDecodeRawTransaction " + arg1 + ' ' + "[tx_hex]" + ' ' + arg3 +"`", inline=False)
		embed.add_field(name="Response:", value=response, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(file=file, embed=embed)
		os.remove('xrDecodeRawTransaction '+ arg1 + ' ' + '[tx_hex]' + ' ' + arg3 + '.json')

	else:

		embed = discord.Embed(title="", description="", timestamp=datetime.datetime.utcnow(), color=0x02c6f8) 

		embed.set_author(name="XRouter API", icon_url="https://pbs.twimg.com/profile_images/1217997394874437632/zG4qMFtP_400x400.jpg")
		embed.add_field(name="Command:", value="`xrDecodeRawTransaction " + arg1 + ' ' + "[tx_hex]" + ' ' + arg3 +"`", inline=False)
		embed.add_field(name="Response:", value=xrDecodeRawTransaction_JSON, inline=False)
		embed.set_footer(text="API Response Timestamp")

		await ctx.send(embed=embed)

client.run('NjA1MjUyMzMyNTM5NzQwMTgw.XUOSsg.fwHQt8hunsoHClaRAmcz-Knp7HU')
