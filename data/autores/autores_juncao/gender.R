
library(genderBR)


df <- read.csv(file = "fullname_all.csv", header = TRUE, sep = ",")

df$gender <- get_gender(df$FULL_NAME)

write.csv(df, file = "atualizado.csv")






