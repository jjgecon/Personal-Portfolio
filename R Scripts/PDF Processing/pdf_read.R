library(pdftools)
library(quanteda)

setwd(XX)

files <- list.files(pattern = "pdf$")

cons_inf <- lapply(files, pdf_text) #Get data per page

list1 = vector(mode = "list", length = length(cons_inf))
names(list1) = files

for (i in 1:length(cons_inf)) {

  # This just gets me the tokens per file
  uni_g = tokens(cons_inf[[i]], what = "word",
                 remove_numbers = TRUE, remove_punct = TRUE,
                 remove_symbols = TRUE, split_hyphens = TRUE)

  uni_g_dfm = dfm(uni_g, tolower = TRUE, stem = FALSE)
  uni_g_dfm = as.matrix(uni_g_dfm)

  #pages
  tp = length(cons_inf[[i]])

  #total words
  tw = sum(uni_g_dfm)

  #total words per page
  tw_pg = apply(uni_g_dfm, 1, sum)

  uni_g_dfm = dfm(uni_g, tolower = TRUE, stem = FALSE, remove = stopwords("spanish"))
  uni_g_dfm = as.matrix(uni_g_dfm)

  #top 10 most popular words
  v = rowSums(t(uni_g_dfm)) %>%
    sort(decreasing = TRUE)

  list1[[i]] = list(tp,tw,tw_pg,head(v,10))

}

# list to dataframe prep
#
df_names = c("Place", "N pages", "Total words", "top 1", "freq", "top 2", "freq",
             "top 3", "freq", "top 4", "freq", "top 5", "freq", "top 6", "freq", "top 7", "freq", "top 8",
             "freq", "top 9", "freq", "top 10", "freq")

rr = length(list1)
cc = length(df_names)

df = matrix(nrow = rr, ncol = cc)
df[,1] = substr(files,1,nchar(files)-4)

for (row in 1:rr) {
  df[row,2] = list1[[row]][[1]]
  df[row,3] = list1[[row]][[2]]
  x = 1
  for (i in seq(4,cc,2)) {
    df[row,i] = names(list1[[row]][[4]][x])
    df[row,i+1] = list1[[row]][[4]][x]
    x = x + 1
  }
}

df = as.data.frame(df)
names(df) = df_names

# exporting to excel
#
write.csv(df, XX)
