import os
from PIL import Image

#https://minzkraut.com/2016/11/23/making-a-simple-spritesheet-generator-in-python/
#https://gist.github.com/gourneau/939252/6f3bee34c4e2becb7684680c58a7343d5be99334

max_columns = 3


def get_frames(file_path):
    imgs = []
    #check if file_name ends with .gif if not print error and exit
    if not file_path.endswith(".gif"):
        print("Error: file_name must end with .gif")
        exit()
        
    img = Image.open(f"{file_path}") 

    rows=0;
    frames = img.n_frames
    
    width, height = img.size
    image_width = width
    image_height = height
    

    for i in range(0,frames):
        if i % max_columns == 0:
            rows += 1


    
    
        #loop through gif frames and save each frame as a png
    for frame in range(0,img.n_frames):
        #get current gif frame and make it image 
        img.seek(frame)
        #add frame to list
        new_img = Image.new(
        mode='RGBA',
        size=(image_width, height),
        color=(0,0,0,0))
        new_img.paste(img,(0,0))
        imgs.append(new_img)
       
    return image_width,image_height,imgs



def export_frames(imgs,file_path,output_folder):
    dir, file_name = os.path.split(file_path)
    image_width=imgs[0].width
    image_height  = imgs[0].height
    frames = len(imgs)
  
    output_dir = f"{dir}{output_folder}/"
    #check if output_dir exists if not create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for frame in range(0,frames):
        imgs[frame].save(f"{output_dir}{file_name}_{frame}.png", format="PNG")

def make_frames(file_path,output_folder="./"):
    
    #check if file_name ends with .gif if not print error and exit
    if not file_path.endswith(".gif"):
        print("Error: file_name must end with .gif")
        exit()

    image_width,image_height,imgs = get_frames(file_path)
    dir, file_name = os.path.split(file_path)

    current_column =0;
    current_row =0;
    rows=0;
    frames = len(imgs)
    

    for i in range(0,frames):
        if i % max_columns == 0:
            rows += 1

    sheet_width = (image_width * max_columns) 
    sheet_height = (image_height * rows) 
    
    sheet = Image.new(
    mode='RGBA',
    size=(sheet_width, sheet_height),
    color=(0,0,0,0))
    
    

    
    output_dir = f"{dir}{output_folder}/"
    #check if output_dir exists if not create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    


    print(frames)
    for frame in range(0,frames):
        f = imgs[frame]
        print(f)
        sheet.paste(imgs[frame].copy(),(image_width*current_column,image_height*current_row))
        current_column += 1
        if current_column % max_columns == 0:
            current_row += 1
            current_column = 0

    # #loop through gif frames and save each frame as a png
    # for frame in range(0,gif.n_frames):
    #     #get current gif frame and make it image 
    #     gif.seek(frame)
    #     sheet.paste(gif,(image_width*current_column,image_height*current_row))
    #     current_column += 1
    #     if current_column % max_columns == 0:
    #         current_row += 1
    #         current_column = 0
  
        
    print(f"img width: {image_width}")
    print(f"img height: {image_height}")
    print(f"sheet width: {sheet_width}")
    print(f"sheet height: {sheet_height}")
    

    file_name = file_name.split(".")[0]
    sheet.save(f"{output_dir}{file_name}_sheet.png", format="PNG")
    #save sheet as a png

    
    
    
    # for frame in range(0,gif.n_frames):
    # gif.seek(frame)
    # sheet.paste(gif.seek(frame),(location,0))
    # gif.save(f"{output_dir}{file_name}_{frame}.png")
    


    # frame_one = frames[0]
    # frame_one.save(f"{output_folder}/{file_name}.gif", format="GIF", append_images=frames,
    #            save_all=True, duration=100, loop=0, transparency=0,disposal=2)


if __name__ == "__main__":
    make_frames("testGifyGif.gif","frames")
