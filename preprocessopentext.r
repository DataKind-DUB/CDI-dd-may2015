library(plyr)
library(tm)
library(SnowballC)
suggestionsforimproverment <- read.csv("~/R_Studies in R/cdi/suggestionsforimproverment.csv",stringsAsFactors = FALSE,na.string=c("Null",""))

df1=suggestionsforimproverment
df1words=df1[,2]

xx=removeWords(df1words, stopwords("english"))
xx=removePunctuation(xx)

yyy=stemDocument(xx)
df1$stopwordsremoved=xx
df1$stoppednstemmed=yyy
#####the function took out all the no's,....they are relevant so I put them back in
df1[c(3,4,17,26,27,29,63,64,102),4]="no"


oththoughts <- read.csv("~/R_Studies in R/cdi/otherthoughts.csv",stringsAsFactors = FALSE,na.string=c("Null",""))

df2=oththoughts
df2words=df1[,2]
df2words=tolower(df2words)
df2words=removePunctuation(df2words)
xx=removeWords(df2words, stopwords("english"))
yyy=stemDocument(xx)
df2$SuggestionsForstopwordsremoved=xx
df2$stoppednstemmed=yyy
#####the function took out all the no's,....they are relevant so I put them back in
df2[c(4,17,27,29,64,93,96,102),]="no"


write.csv(df1,file="suggestionsForImprovement.csv")
write.csv(df2,file="oththoughts.csv")


####Create TermDocument Matrix For Suggestions For Improvement
myCorpus <- Corpus(VectorSource(df1[,2]))
tdm <- TermDocumentMatrix(myCorpus, control = list(removePunctuation = TRUE, stopwords=TRUE))
inspect(tdm)


####Create TermDocument Matrix For OtherThoughts
myCorpus2 <- Corpus(VectorSource(df2[,2]))
tdm2 <- TermDocumentMatrix(myCorpus, control = list(removePunctuation = TRUE, stopwords=TRUE))
inspect(tdm)
