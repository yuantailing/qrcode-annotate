import com.google.zxing.*;
import com.google.zxing.common.*;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import javax.imageio.*;
import java.awt.image.BufferedImage;
import com.google.zxing.qrcode.QRCodeReader;
import com.google.zxing.qrcode.QRCodeWriter;
import com.google.zxing.qrcode.decoder.Decoder;
import com.google.zxing.qrcode.decoder.ErrorCorrectionLevel;
import com.google.zxing.qrcode.decoder.Version;
import com.google.zxing.qrcode.detector.Detector;
import com.google.zxing.BufferedImageLuminanceSource;

public class Main {
    public static void main(String args[]) throws Exception {
        String imgs_root = "../../qrcode-annotate/wrapped";
        File[] fileList = new File(imgs_root).listFiles();
        for (int i_file = 0; i_file < fileList.length; i_file++) {
            BufferedImage image = ImageIO.read(fileList[i_file]);
            LuminanceSource source = new BufferedImageLuminanceSource(image);
            Binarizer binarizer = new HybridBinarizer(source);
            BinaryBitmap binaryBitmap = new BinaryBitmap(binarizer);

            Map<DecodeHintType, Object> hints = new EnumMap<>(DecodeHintType.class);
            hints.put(DecodeHintType.TRY_HARDER, Boolean.TRUE);
            boolean detect_success = false;
            boolean decode_success = false;
            BitMatrix bits = new BitMatrix(1);

            try {
                DetectorResult detectorResult = new Detector(binaryBitmap.getBlackMatrix()).detect(hints);
                bits = detectorResult.getBits();
                detect_success = true;
            } catch (com.google.zxing.NotFoundException e) {
            } catch (com.google.zxing.FormatException e) {
            }

            try {
                QRCodeReader reader = new QRCodeReader();
                reader.decode(binaryBitmap, hints);
                decode_success = true;
            } catch (com.google.zxing.NotFoundException e) {
            } catch (com.google.zxing.FormatException e) {
            } catch (com.google.zxing.ChecksumException e) {
            }
            
            if (detect_success) {
                System.out.print(fileList[i_file].getName() + " ");
                System.out.print(decode_success ? "success" : "failure");
                System.out.print(" ");
                int width = bits.getWidth();
                int height = bits.getHeight();
                for (int i = 0; i < height; i++) {
                    for (int j = 0; j < width; j++)
                        System.out.print(bits.get(j, i) ? 1 : 0);
                }
                System.out.println();
            }
        }
    }
}
