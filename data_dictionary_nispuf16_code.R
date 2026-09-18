load("NISPUF16.RData")

labels <- sapply(
  NISPUF16,
  function(x) attr(x, "label")
)

dictionary <- data.frame(
  variable = names(NISPUF16),
  description = unname(labels)
)

write.csv(
  dictionary,
  "nispuf16_data_dictionary.csv",
  row.names = FALSE
)