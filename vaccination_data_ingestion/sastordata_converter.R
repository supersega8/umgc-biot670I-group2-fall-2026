library(SAScii)
# SAScii package can read SAS statements, and enable R to process the statements and .DAT file to an RData file 
data_path <- readline(
  prompt = "Enter the filepath for the dat files: "
)

sas_scripts <- readline(
  prompt = "Enter the filepath where the SAS script files are: "
)

Rdata_path <- readline(
  prompt = "Where should the RData file go?: "
)

#can edit to select years
datfilelist <- c(
  '95','96','97','98','99',
  '00','01','02','03','04','05'
)

dat_list <- list.files(
  path = data_path,
  pattern = "\\.DAT$",
  full.names = TRUE,
  ignore.case = TRUE
)

sas_list <- list.files(
  path = sas_scripts,
  pattern = "\\.SAS$",
  full.names = TRUE,
  ignore.case = TRUE
)

for (i in datfilelist) {
  
  for (datfile in dat_list) {
    
    for (sasfile in sas_list) {
      
      if (
        grepl(i, basename(datfile), fixed = TRUE) &&
        grepl(i, basename(sasfile), fixed = TRUE)
      ) {
        
        sas_lines <- readLines(sasfile, warn = FALSE)
        
        #need to use this otherwise R throws an error, the input_line is the starting line
        input_line <- grep(
          "^\\s*INPUT\\b",
          sas_lines,
          ignore.case = TRUE,
          perl = TRUE
        )[1]
        
       
        
        print(paste("Processing year", i))
        print(datfile)
        print(sasfile)
        
        data_read <- read.SAScii(
          fn = datfile,
          sas_ri = sasfile,
          beginline = input_line
        )
        
        save(
          data_read,
          file = file.path(
            Rdata_path,
            paste0("NISPUF", i, ".RData")
          )
        )
        
        print(paste("Finished year", i))
      }
    }
  }
}

