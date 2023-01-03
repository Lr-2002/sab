import asyncio
from scihub import SciHub
from gooey import Gooey, GooeyParser


def search(keywords: str, limit: int, path: str):
    """
  搜索相关论文并下载
  Args:
      keywords (str): 关键词
      limit (int): 篇数
      path (str): 下载路径
  """
    sh = SciHub()
    result = sh.search(keywords, limit=limit)
    print(result)

    loop = asyncio.get_event_loop()
    # 获取所有需要下载的scihub直链
    tasks = [sh.async_get_direct_url(paper["url"]) for paper in result.get("papers", [])]
    all_direct_urls = loop.run_until_complete(asyncio.gather(*tasks))
    print(all_direct_urls)

    # 下载所有论文
    loop.run_until_complete(sh.async_download(loop, all_direct_urls, path=path))
    loop.close()


@Gooey
def main():
    parser = GooeyParser(description="中文环境可用的scihub下载器 - @Python实用宝典")
    parser.add_argument('path', help="下载路径", widget="DirChooser")
    parser.add_argument('keywords', help="关键词")
    parser.add_argument('limit', help="下载篇数")
    args = parser.parse_args()
    search(args.keywords, int(args.limit), args.path)


main()