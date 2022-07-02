import discord
from discord.ext import commands

token = "Your Discord Bot Token"

intents = discord.Intents().default()
intents.members = True

# client = discord.Client()
client = commands.Bot(command_prefix=".", intents=intents)
client.remove_command("help")


def check(ctx):
    return lambda m: m.author == ctx.author and m.channel == ctx.channel


async def get_input_of_type(func, ctx):
    while True:
        try:
            msg = await client.wait_for('message', check=check(ctx))
            return func(msg.content)
        except ValueError:
            continue


async def bubbleSort(ctx, array, display):
    message = await ctx.send("Bubble Sort Algorithm; Time Complexity: O(n^2); Space Complexity: O(1)")
    for i in range(len(array)):
        isSolved = True
        for j in range(len(array) - 1):
            if array[j] > array[j + 1]:
                if display:
                    await message.edit(content=f"{message.content}\n``{array}`` --> {array[j]} is bigger than {array[j+1]}.. Swapping")
                array[j], array[j + 1] = array[j + 1], array[j]
                isSolved = False
            print(array)
        if isSolved:
            break
    return array


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(name=".sort", type=2))
    print(f'{client.user} has connected to Discord!')


@client.command()
async def sort(ctx):
    try:
        await ctx.send("Enter the numbers you want to sort separated by spaces")
        numbers = await get_input_of_type(lambda x: [int(i) for i in x.split()], ctx)
        await ctx.send("Do you want to see the sorting process? (y/n)")
        display = await get_input_of_type(str, ctx)
        if display.lower() == "y":
            display = True
        else:
            display = False
        await ctx.send("1. Bubble Sort\n2. Merge Sort\n3. Suggest a sorting algorithm")
        option = await get_input_of_type(int, ctx)
        if option == 1:
            await ctx.send(f"Sorted: {await bubbleSort(ctx, numbers, display)}")
        elif option == 2:
            await ctx.send("Not implemented yet")
        elif option == 3:
            await ctx.send("Not implemented yet")
        else:
            await ctx.send("Invalid option")
    except Exception as e:
        await ctx.send(f"Something went wrong: {e}")


print("Connecting to discord...")
client.run(token, reconnect=True)
