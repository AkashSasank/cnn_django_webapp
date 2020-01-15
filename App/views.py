from django.shortcuts import render
from .forms import PhotoUploadForm
from .models import Photo
from keras.applications.mobilenet_v2 import MobileNetV2, decode_predictions, preprocess_input
from keras.preprocessing.image import load_img, img_to_array
import cnn_webapp.settings as settings


# Create your views here.


def home(request):
    prediction = ''
    src = ''
    flag = 1
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            model = MobileNetV2()
            prediction = predict(model)
            flag = 0
            return render(request, 'App/index.html', {
                'form': form, 'prediction': prediction, 'src': src, "flag": flag
            })
    else:
        form = PhotoUploadForm()
    return render(request, 'App/index.html', {
        'form': form, 'prediction': prediction, 'src': src, "flag": flag
    })


def predict(model):
    photo = Photo.objects.values_list('document').order_by('-uploaded_at')[0][0]
    src = settings.MEDIA_URL + photo
    image = load_img(settings.BASE_DIR + src, target_size=(224, 224))
    image = img_to_array(image)
    input_image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    input_image = preprocess_input(input_image)
    prediction = model.predict(input_image)
    label = decode_predictions(prediction)[0][0]
    return '{} {}'.format(label[1], label[2] * 100)
