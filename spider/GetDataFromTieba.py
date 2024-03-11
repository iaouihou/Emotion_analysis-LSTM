import csv
import asyncio
import aiotieba

async def extract_post_info(post):
    text_content = post.text
    userid = post.user.user_id
    user_name = post.user.user_name
    nick_name_new = post.user.nick_name_new
    ip_address = post.user.ip
    return text_content, userid, user_name, nick_name_new,ip_address

async def write_posts_to_csv(posts, file_name):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["内容", "用户ID", "用户名", "IP地址"])
        for post in posts:
            text, userid, user_name, ip_address = await extract_post_info(post)
            writer.writerow([text, userid, user_name, ip_address])
    print("数据已写入", file_name)

async def write_posts_to_csv(posts, filename):
    with open(filename, mode='w', encoding='utf-8-sig', newline='') as file:
        # 写入 CSV 文件的代码
        writer = csv.writer(file)
        writer.writerow(['Text', 'User ID', 'User Name', 'Nick Name New', 'IP Address'])
        for post in posts:
            text, user_id, user_name, nick_name_new, ip_address = await extract_post_info(post)
            if text:  # 检查text内容是否为空
                writer.writerow([text, user_id, user_name, nick_name_new, ip_address])


async def main():
    async with aiotieba.Client() as client:
        posts = await client.get_posts(8506516164,rn=60,with_comments = True)
        await write_posts_to_csv(posts, 'posts.csv')



if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
