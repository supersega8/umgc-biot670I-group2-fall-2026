#Load the file path here 

file_path <- readline(prompt = r"(Enter the filepath for the R files: )")

#list all the R_data files
file_list <- list.files(
  path = file_path,
  pattern = "\\.RData$",
  full.names = TRUE
)

#creates the labels_list here to build the labels for the dictionary later on

labels_list <- list()
#dictionary data- contains the file, year, variable, and description for each NIS dataset
dictionary <- data.frame(
  file = character(),
  year = integer(),
  variable = character(),
  description = character()
)
#nested loops that go into each file to find the relevant labels
for (file in file_list) {
  
  file_name <- basename(file)
  
  # Extract the 2-digit year from something like NISPUF16.RData
  year_short <- as.integer(
    sub(".*NISPUF([0-9]{2}).*", "\\1", file_name)
  )
  
  # Convert to four-digit year
  year <- ifelse(
    year_short >= 90,
    1900 + year_short,
    2000 + year_short
  )
  
  labels_list[[file_name]] <- list()
  
  loaded_objects <- load(file)
  
  for (obj_name in loaded_objects) {
    
    obj <- get(obj_name)
    
    if (is.data.frame(obj)) {
      
      labels_list[[file_name]][[obj_name]] <- list()
      
      for (column_name in names(obj)) {
        
        column <- obj[[column_name]]
        label <- attr(column, "label")
        
        labels_list[[file_name]][[obj_name]][[column_name]] <- label
        
        dictionary <- rbind(
          dictionary,
          data.frame(
            file = file_name,
            year = year,
            variable = column_name,
            description = if (is.null(label)) NA else as.character(label)
          )
        )
      }
    }
  }
}

write.csv(
  dictionary,
  "NIS_dictionary.csv",
  row.names = FALSE
)





