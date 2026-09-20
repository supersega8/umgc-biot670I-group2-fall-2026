# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 21:51:53 2026

@author: sumit
"""

from pathlib import Path
import subprocess
import time

"""This is the index of files, 2015 was skipped since there were no R data files for that particular year. R data files started around 2006. Prior to that it was all
SAS (from 1995-2005)"""
#need to convert sc
index = ['06', '07', '08', '09',
'10', '11', '12', '13', '14',
 '16', '17', '18', '19',
'20', '21', '22', '23', '24']


#Data analyzer, checks to see if the R files exist first, then does some code manipulation with R, finally
#running a subprocess to run R in the python console to generate final R data files 
#handles under class dataanalyzer with three functions
class dataanalyzer:

    def __init__(self, rdata_folder, dat_folder, r_folder):

        self.rdata_folder = Path(rdata_folder)
        self.dat_folder = Path(dat_folder)
        self.r_folder = Path(r_folder)


    def R_file_analyzer(self, index):

        for number in index:

            filepath = self.r_folder / f"NISPUF{number}.R"

            if filepath.exists():
                print(f"NISPUF{number}.R exists")

            else:
                print("error, file doesn't exist!")
                raise RuntimeError(
                    f"NISPUF{number}.R does not exist"
                )

        return "done"


    def Rdata_modification(self, index):

        for number in index:
           
        #    if number=='23':
        #        old_PUF = 'PUF <- "path-to-file"'
        #    else:
       #         old_PUF = 'PUF <- "path-to-data"'
              
            
                
            filepath = self.r_folder / f"NISPUF{number}.R"

            dat_filepath = (
                self.dat_folder /
                f"NISPUF{number}.DAT"
            )

            filecontent = filepath.read_text().splitlines()
            new_filecontent=[]
            
            for line in filecontent:
                if line.strip().startswith(r'PUF <-'):
                    line = f'PUF <- "{self.rdata_folder.as_posix()}"'
                    
                elif line.strip().startswith(r'flatfile <-'):
                   line = f'flatfile <- "{dat_filepath.as_posix()}"'
                        
                new_filecontent.append(line)
            

           
            modified_filepath = (
                self.r_folder /
                f"NISPUF{number}_modified.R"
            )

            modified_filepath.write_text("\n".join(new_filecontent))

            print(
                f"Updated NISPUF{number}.R"
            )
            


    def R2Rdata(self, index):

        
            total=len(index)
            start=time.time()
          
            for i,number in enumerate(index,start=1):
    
                filepath = (
                        self.r_folder /
                        f"NISPUF{number}_modified.R"
                    )
                    
                print(f"Starting R script for NISPUF{number}...")
                        
                try:  
        
                    command = [
                                r"C:\Program Files\R\R-4.5.1\bin\Rscript.exe",
                                str(filepath)
                            ]
                            
                       
                        
                    result=subprocess.run(
                                command,
                                text=True,
                                check=True,
                                capture_output=True
                            )
                    print(result.stdout)
                    print(result.stderr)
                            
                    elapsed=time.time()-start
                    percent = (i / total) * 100
                            
                    print(
               f"[{i}/{total}] NISPUF{number} complete "
               f"({percent:.1f}%) - {elapsed / 60:.1f} minutes"
           )
            
                    print(
                                f"Successfully ran script for index {number}"
            
                            )
                            
                            
                    

                except subprocess.CalledProcessError as e:
    
                    print(
                    f"Script failed at index {number} with error: {e.stderr}"
                   
                   
                
                )
                    continue


analyzer = dataanalyzer(
    rdata_folder=
    input(r"Tell me the files where the R data should be stored: "),

    dat_folder=
    input(r"Tell me where the DAT folder is: "),

    r_folder=
    input(r"Tell me where the R script files are: ")
)


if __name__ == "__main__":

    try:
    
        analyzer.R_file_analyzer(index)
    
        analyzer.Rdata_modification(index)
    
        analyzer.R2Rdata(index)
    
    except RuntimeError as error:
    
        print(
            f"There was an error! {error}"
        )