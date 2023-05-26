#include <filesystem>
#include <opencv2/opencv.hpp>

// const std::string kImageDir = "/path/to/your/images";
// const std::string kOutputDir = "/path/to/your/images/compressed";

void ProcessImage(const std::string &input_path, const std::string &output_path) {
    cv::Mat img = cv::imread(input_path, cv::IMREAD_GRAYSCALE);

    if (!img.data) {
        std::cout << "Could not open or find the image: " << input_path << std::endl;
        return;
    }

    // Expand the image to an optimal size
    cv::Mat padded;
    int m = cv::getOptimalDFTSize(img.rows);
    int n = cv::getOptimalDFTSize(img.cols);
    cv::copyMakeBorder(img, padded, 0, m - img.rows, 0, n - img.cols, cv::BORDER_CONSTANT, cv::Scalar::all(0));

    // Make place for both the complex and the real values
    cv::Mat planes[] = {cv::Mat_<float>(padded), cv::Mat::zeros(padded.size(), CV_32F)};
    cv::Mat complexI;
    cv::merge(planes, 2, complexI);

    // Make the Discrete Fourier Transform
    cv::dft(complexI, complexI);

    // Transform the real and complex values to magnitude
    cv::split(complexI, planes);
    cv::magnitude(planes[0], planes[1], planes[0]);
    cv::Mat magI = planes[0];

    // Switch to a logarithmic scale
    magI += cv::Scalar::all(1);
    cv::log(magI, magI);

    // Crop and rearrange
    magI = magI(cv::Rect(0, 0, magI.cols & -2, magI.rows & -2));
    int cx = magI.cols / 2;
    int cy = magI.rows / 2;

    cv::Mat q0(magI, cv::Rect(0, 0, cx, cy));   // Top-Left
    cv::Mat q1(magI, cv::Rect(cx, 0, cx, cy));  // Top-Right
    cv::Mat q2(magI, cv::Rect(0, cy, cx, cy));  // Bottom-Left
    cv::Mat q3(magI, cv::Rect(cx, cy, cx, cy)); // Bottom-Right

    cv::Mat tmp;
    q0.copyTo(tmp);
    q3.copyTo(q0);
    tmp.copyTo(q3);

    q1.copyTo(tmp);
    q2.copyTo(q1);
    tmp.copyTo(q2);

    // Normalize the result
    cv::normalize(magI, magI, 0, 255, cv::NORM_MINMAX, CV_8U);

    // Save the transformed image
    cv::imwrite(output_path, magI);
}

int main(int argc, char* argv[]) {
    if(argc < 3) {
        std::cout << "Usage: ./compress_image <input_dir> <output_dir>" << std::endl;
        return 1;
    }

    std::string kImageDir = argv[1];
    std::string kOutputDir = argv[2];

    if(!std::filesystem::exists(kImageDir)) {
        std::cout << "Input directory does not exist." << std::endl;
        return 1;
    }
    
    if(!std::filesystem::exists(kOutputDir)) {
        std::filesystem::create_directory(kOutputDir);
    }

    for (const auto& entry : std::filesystem::directory_iterator(kImageDir)) {
        if (entry.is_regular_file() && entry.path().extension() == ".png") {
            std::string output_path = kOutputDir + "/" + entry.path().stem().string() + "_compressed.png";
            ProcessImage(entry.path().string(), output_path);
        }
    }

    return 0;
}

