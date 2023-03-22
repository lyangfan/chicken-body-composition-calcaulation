import SimpleITK as sitk
import numpy as np


def load_dicom_series_as_sitk_img(dicom_dir):
    '''
    Load dicom series as SimpleITK.Image.

    param dicom_dir: the dicom series directory. (type: str)

    return:
    image: the SimpleITK image of the dicom series. (type: class SimpleITK.Image)
    '''
    reader = sitk.ImageSeriesReader()
    dicom_series_name = reader.GetGDCMSeriesFileNames(dicom_dir)
    reader.SetFileNames(dicom_series_name)
    image = reader.Execute()
    return image

def load_nifti_file_as_sitk_img(nifti_file):
    '''
    Load nifti file as SimpleITK.Image.

    param nifti_file: the nifti file path. (type: str)

    return:
    image: the SimpleITK image of the nifti file. (type: class SimpleITK.Image)   
    '''
    reader = sitk.ImageFileReader()
    reader.SetImageIO('NiftiImageIO')
    reader.SetFileName(nifti_file)
    image = reader.Execute()
    return image

def get_sitk_image_parameters(sitk_image):
    '''
    Get the spacing, origin and direction of the SimpleITK.Image.

    param sitk_image: the SimpleITK image. (type: class SimpleITK.Image)

    return:
    spacing, origin, direction: the spacing, origin and direction of the image. (type: tuple)
    '''
    spacing = sitk_image.GetSpacing()
    origin = sitk_image.GetOrigin()
    direction = sitk_image.GetDirection()
    return spacing, origin, direction

def have_same_parameters(sitk_image1, sitk_image2):
    '''
    Determine whether two SimpleITK.Image have the same spacing, origin and direction.

    param sitk_image1: the SimpleITK image. (type: class SimpleITK.Image)
    param sitk_image2: the SimpleITK image. (type: class SimpleITK.Image)

    return:
    type: bool
    '''
    return get_sitk_image_parameters(sitk_image1) == get_sitk_image_parameters(sitk_image2)

def calculate_vol_using_label(source_dicom_dir, label_nifti_file, target_label_id):
    '''
    Calculate the target part volume(unit: dm3) using label.

    param source_dicom_dir: the dicom series folder. (type: str)
    param label_nifti_file: the label nifti file. (type: str)
    param target_label_id: the target part id of the label nifti file. (type: int)

    return:
    the volume of the target part(unit: dm3) (type: float)
    '''
    source_img = load_dicom_series_as_sitk_img(source_dicom_dir)
    label_img = load_nifti_file_as_sitk_img(label_nifti_file)
    spacing = get_sitk_image_parameters(source_img)[0]
    if have_same_parameters(source_img, label_img):
        label_array = sitk.GetArrayFromImage(label_img)
        voxel_sum = np.sum(label_array == target_label_id)
        volume = voxel_sum * spacing[0] * spacing[1] * spacing[2] / (10 ** 6)
        return volume
    else:
        raise ValueError('The parameters of the label are different from those of the dicom files')
    
def main():
    individual_1_dicom_folder = r'E:\data\CT\dicom\individual_1'
    individual_1_label_body = r'E:\data\CT\label\individual_1\body.nii.gz'
    individual_1_label_abdominal_fat = r'E:\data\CT\label\individual_1\abdominal_fat.nii.gz'
    individual_2_dicom_folder = r'E:\data\CT\dicom\individual_2'
    individual_2_label_body = r'E:\data\CT\label\individual_2\body.nii.gz'
    individual_2_label_abdominal_fat = r'E:\data\CT\label\individual_2\abdominal_fat.nii.gz'
    body_id = 1
    abdominal_id = 1
    print("individual 1's body volume is {}".format(calculate_vol_using_label(individual_1_dicom_folder, individual_1_label_body, body_id)))
    print("individual 1's abdominal fat volume is {}".format(calculate_vol_using_label(individual_1_dicom_folder, individual_1_label_abdominal_fat, abdominal_id)))
    print("individual 2's body volume is {}".format(calculate_vol_using_label(individual_2_dicom_folder, individual_2_label_body, body_id)))
    print("individual 2's abdominal fat volume is {}".format(calculate_vol_using_label(individual_2_dicom_folder, individual_2_label_abdominal_fat, abdominal_id)))
    
 
if __name__ == '__main__':
    main()
