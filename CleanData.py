def get_rid_of_empty_line(news_before_clean, news_after_clean):
    news = open(news_before_clean, "r")
    news_cleaned = open(news_after_clean, "w")
    for line in news:
        if(line!="" and line!="\n"):
            news_cleaned.writelines(line)
    news_cleaned.close()
    news.close()

if __name__ == '__main__':
    news_before_clean = "SinaNews_Ori.txt"
    news_after_clean = "Sina News.txt"
    get_rid_of_empty_line(news_before_clean, news_after_clean)