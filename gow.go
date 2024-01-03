/*
This is a command line interface program that allows me to quickly check the weather
without having to leave the terminal or slowing down my workflow.
*/
package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"
)

type Weather struct {
	Location struct {
		Name   string `json:"name"`
		Region string `json:"region"`
	} `json:"location"`
	Current struct {
		FeelsTempF float64 `json:"feelslike_f"`
		Condition  struct {
			Text string `json:"text"`
		} `json:"condition"`
	} `json:"current"`
	Forecast struct {
		Forecastday []struct {
			Hour []struct {
				TimeEpoch  int64   `json:"time_epoch"`
				FeelsTempF float64 `json:"feelslike_f"`
				Condition  struct {
					Text string `json:"text"`
				} `json:"condition"`
				ChanceOfRain float64 `json:"chance_of_rain"`
			} `json:"hour"`
		} `json:"forecastday"`
	} `json:"forecast"`
}

func main() {
	q := "35243"

	if len(os.Args) >= 2 {
		q = os.Args[1]

	}

	res, err := http.Get("http://api.weatherapi.com/v1/forecast.json?key=1190d32c462549e0b41213303240201&q=" + q + "&days=1&aqi=no&alerts-no")
	if err != nil {
		panic(err)
	}

	defer res.Body.Close()

	if res.StatusCode != 200 {
		panic("Weather API not currently available")
	}

	body, err := io.ReadAll(res.Body)
	if err != nil {
		panic(err)
	}

	var weather Weather
	err = json.Unmarshal(body, &weather)
	if err != nil {
		panic(err)
	}

	location, current, hours := weather.Location, weather.Current, weather.Forecast.Forecastday[0].Hour

	fmt.Printf(
		"%s, %s: %.0fF, %s\n",
		location.Name,
		location.Region,
		current.FeelsTempF,
		current.Condition.Text,
	)

	fmt.Println("Time      FeelsLike      Chance of Rain    Condition")

	for _, hour := range hours {
		date := time.Unix(hour.TimeEpoch, 0)
		formatted_date := date.Format("15:04")

		if date.Before(time.Now()) {
			continue
		}

		fmt.Printf(
			"%5s  %5.0fF %10.0f%% %20s\n",
			formatted_date,
			hour.FeelsTempF,
			hour.ChanceOfRain,
			hour.Condition.Text,
		)
	}

}
