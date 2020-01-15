from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from keras.applications.mobilenet_v2 import MobileNetV2, decode_predictions, preprocess_input
from keras.preprocessing.image import load_img, img_to_array
import cnn_webapp.settings as settings


# Create your views here.


def home(request):
    prediction = ''
    src = ''
    flag = 1
    if request.method == 'POST' and request.FILES.get('document'):
        document = request.FILES['document']
        fs = FileSystemStorage()
        filename = fs.save(document.name, document)
        uploaded_file_url = fs.url(filename)
        model = MobileNetV2()
        prediction = predict(model, uploaded_file_url)
        print(filename)
        flag = 0
        return render(request, 'App/index.html', {
         'prediction': prediction, 'src': src, "flag": flag
        })
    return render(request, 'App/index.html', {
        'prediction': prediction, 'src': src, "flag": flag
    })


def predict(model, filename):
    # src = settings.MEDIA_URL + filename
    image = load_img(settings.BASE_DIR + filename, target_size=(224, 224))
    image = img_to_array(image)
    input_image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    input_image = preprocess_input(input_image)
    prediction = model.predict(input_image)
    label = decode_predictions(prediction)[0][0]
    return '{} {}'.format(label[1], label[2] * 100)
