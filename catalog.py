from downloader import *

class DownloaderFromCatalog:
    def __init__(self):
        self.bf = BeautifulSoup(requests.get('https://www.manhuagui.com/list').content, 'html.parser')
        self.getCatMap()

    def getCatMap(self):
        self.catMap = {}
        for i in self.bf.find("div", class_='filter-nav').children:
            self.catMap[i.find('label', recursive=False).text] = {j.text: j.get('href') for j in i.findAll('a')}

    def catExist(self, catalog, catType):
        catType += '：'
        return catalog in self.catMap.get(catType).keys()

    def downloadAllFromCat(self, catalog, catType, path):
        if self.catExist(catalog, catType):
            endpoint = self.catMap.get(catType + '：').get(catalog)
            url = 'https://www.manhuagui.com' + endpoint
            nbf = BeautifulSoup(requests.get(url).content, 'html.parser')
            # 第一页
            # TODO 翻页
            # TODO 中途失败记录offset
            # TODO 优化一下请求网页的效率，考虑缓存关键信息
            for i in nbf.find("div", class_='book-list').findAll('a'):
                addresss = i.get('href')
                downloader = MangaDownloader(addresss, path)
                for j in range(downloader.length):
                    downloader.downloadChapter(downloader.chapters[j][1])
                    print('start to download chapter ' + downloader.chapters[j][0])


if __name__ == '__main__':
    print()
